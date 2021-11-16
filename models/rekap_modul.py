from odoo import models, fields


class rekap_modul(models.Model):
    _name = 'rekap.modul'
    _auto = False
    _description = 'Rekapan Modul Model'

    id_modul = fields.Integer(string="Module ID", required=True)
    nama_modul = fields.Char(size=255, string="Module Name", required=True)
    total_siswa = fields.Integer(string="Total Students", required=True)
    avg_score = fields.Float(string="Average Score", required=True)
    max_score = fields.Float(string="Highest Score", required=True)
    min_score = fields.Float(string="Lowest Score", required=True)
    rating = fields.Float(string="Rating", required=True)

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):
        return """
        SELECT
            nilai_summary.id_modul AS id,
            nilai_summary.id_modul AS id_modul,
            nama_modul,
            total_siswa,
            avg_score,
            max_score,
            min_score,
            rating
        FROM
	    (
	        SELECT
	            id_modul,
                avg(nilai) AS avg_score,
                max(nilai) AS max_score,
                min(nilai) AS min_score,
                count(nilai) AS total_siswa
            FROM
                nilai
            GROUP BY
                id_modul) AS nilai_summary
	        INNER JOIN
	    (
	        SELECT
	            modul.id_modul,
                modul.nama_modul,
                review_modul.avg_rating AS rating
            FROM modul
	        NATURAL JOIN
            (
                SELECT
                    id_modul,
                    avg(rating) AS avg_rating
                FROM
                    review
                GROUP BY
                    id_modul) AS review_modul
	    ) AS review_summary
        ON
            nilai_summary.id_modul = review_summary.id_modul
            """

    def init(self):
        self.env.cr.execute(
            """CREATE OR REPLACE VIEW %s as (%s)""" % (
                self._table, self._query())
        )

        self.env.cr.execute(
            """CREATE OR REPLACE FUNCTION update_rekap()
                RETURNS TRIGGER LANGUAGE plpgsql
                AS $$
                BEGIN
                CREATE OR REPLACE VIEW %s as (%s
                );
                RETURN NULL;
                END $$
                """ % (self._table, self._query())
        )

        self.env.cr.execute(
            """DROP TRIGGER IF EXISTS
                nilai_insert
                ON nilai
                """
        )

        self.env.cr.execute(
            """DROP TRIGGER IF EXISTS
                review_insert
                ON review
                """
        )

        self.env.cr.execute(
            """CREATE TRIGGER nilai_insert
	            AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE
	            ON nilai
                EXECUTE PROCEDURE update_rekap()"""
        )

        self.env.cr.execute(
            """CREATE TRIGGER review_insert
	            AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE
	            ON review
                EXECUTE PROCEDURE update_rekap()"""
        )


class rekap_summary(models.Model):
    _name = 'rekap.summary'
    _auto = False
    _description = 'Rekapan Modul Summary'

    min_score = fields.Float(string="Lowest Score", required=True)
    min_modul = fields.Char(string="Lowest Score Modul", required=True)
    high_score = fields.Float(string="Highest Score", required=True)
    high_modul = fields.Char(string="Highest Score Modul", required=True)

    avg_rating = fields.Float(string="Average Rating", required=True)
    avg_score = fields.Float(string="Average Score", required=True)
    total_student = fields.Integer(string="Total Students", required=True)
    total_review = fields.Integer(string="Total Reviews", required=True)

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):
        return """
        SELECT 
            1 as id,
	        min_score,
	        min_modul,
	        high_score,
	        high_modul,
	        avg_rating,
	        avg_score,
	        total_student,
	        getReview() as total_review
        FROM
	        getMin() as (min_score float, min_modul varchar),
	        getSummary() as (avg_rating FLOAT, avg_score FLOAT, total_student INT),
	        getMax() as (high_score FLOAT, high_modul varchar)
            """
    
    def init(self):
        self.env.cr.execute(
            """
            CREATE OR REPLACE FUNCTION getMin()
            RETURNS RECORD AS $$
            DECLARE ret RECORD;
            BEGIN
            SELECT 
                min_score, 
                nama_modul 
            FROM 
                rekap_modul 
            WHERE 
                min_score in (
                                SELECT 
                                    min(min_score) 
                                FROM 
                                    rekap_modul
                            )
                            INTO ret;
            RETURN ret;
            END;$$  LANGUAGE plpgsql
            """
        )

        self.env.cr.execute(
            """
            CREATE OR REPLACE FUNCTION getMax()
	        RETURNS RECORD AS $$
	        DECLARE ret RECORD;
            BEGIN
	        SELECT 
                max_score, 
                nama_modul 
	        FROM rekap_modul 
	        WHERE 
                max_score in (
                                SELECT 
                                    max(max_score) 
                                FROM 
                                    rekap_modul
                            )
	                        INTO ret;
	        RETURN ret;
            END;$$  LANGUAGE plpgsql
            
            """
        )

        self.env.cr.execute(
            """
            CREATE OR REPLACE FUNCTION getSummary() RETURNS RECORD AS $$
            DECLARE  ret RECORD;
            BEGIN
	        SELECT 
                avg(rating)::FLOAT, 
                avg(avg_score)::FLOAT, 
                sum(total_siswa)::INT 
            FROM 
                rekap_modul 
            INTO ret;
            RETURN ret;
            END;$$ LANGUAGE plpgsql
            """
        )

        self.env.cr.execute(
            """
            CREATE OR REPLACE FUNCTION getSummary() RETURNS RECORD AS $$
            DECLARE  ret RECORD;
            BEGIN
	        SELECT 
                avg(rating)::FLOAT, 
                avg(avg_score)::FLOAT, 
                sum(total_siswa)::INT 
            FROM 
                rekap_modul 
            INTO ret;
            RETURN ret;
            END;$$ LANGUAGE plpgsql
            """
        )

        self.env.cr.execute(
            """
            CREATE OR REPLACE FUNCTION getReview()
	        RETURNS INTEGER LANGUAGE plpgsql AS $$
            BEGIN
	        RETURN 
            (
                SELECT 
                    COUNT(*) 
                FROM review
            );
            END $$"""
        )

        self.env.cr.execute(
            """CREATE OR REPLACE VIEW %s as (%s)""" % (
                self._table, self._query())
        )

        self.env.cr.execute(
            """CREATE OR REPLACE FUNCTION update_summary()
                RETURNS TRIGGER LANGUAGE plpgsql
                AS $$
                BEGIN
                CREATE OR REPLACE VIEW %s as (%s
                );
                RETURN NULL;
                END $$
                """ % (self._table, self._query())
        )

        self.env.cr.execute(
            """
            DROP TRIGGER IF EXISTS summary_change
            ON rekap_modul
            """
        )

        self.env.cr.execute(
            """CREATE TRIGGER summary_change
	            AFTER INSERT OR UPDATE OR DELETE
	            ON rekap_modul
                EXECUTE PROCEDURE update_summary()"""
        )