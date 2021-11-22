from odoo import models, fields


class siswa(models.Model):
    _name = 'siswa'
    _description = 'Siswa'

    id_siswa = fields.Integer(string="ID Siswa", required=True)
    batch = fields.Integer(string="Batch", required=True)
    nama = fields.Char(size=255, string="Nama", required=True)
    email = fields.Char(size=255, string="Email", required=True)
    work = fields.Char(size=255, string="Pekerjaan", required=True)
    education = fields.Char(size=255, string="Pendidikkan Terakhir", required=True)
    usia = fields.Integer(string="Usia", required=True)
    pwd = fields.Text(string="Password", required=True)

class modul(models.Model):
    _name = 'modul'
    _description = 'Modul'

    id_modul = fields.Integer(string="ID Modul", required=True)
    nama_modul = fields.Char(size=255, string="Nama Modul", required=True)


class nilai(models.Model):
    _name = 'nilai'
    _description = 'Nilai'

    id_siswa = fields.Many2one('siswa', string="ID Siswa", required=True)
    id_modul = fields.Many2one('modul', string="ID Modul", required=True)
    nilai = fields.Float(string="Nilai", required=True)
    time = fields.Date(string="Tanggal", required=True)


class review(models.Model):
    _name = 'review'
    _description = 'Review'

    id_siswa = fields.Many2one('siswa', string="ID Siswa", required=True)
    id_modul = fields.Many2one('modul', string="ID Modul", required=True)
    rating = fields.Float(string="Rating", required=True)

class rekap_siswa(models.Model):
    _name = 'rekap.siswa'
    _auto = False
    _description = 'Rekapan Nilai Siswa'


    month = fields.Date(string="Bulan", required=True)
    total_siswa = fields.Integer(string="total Siswa", required=True)
    total_nilai = fields.Float(string="total nilai", required=True)
    rata_rata = fields.Float(string="rata rata", required=True)

    def _query(self):
        return """
        SELECT
        row_number() over () as id,
        month, total_siswa, total_nilai,
        total_nilai/total_siswa AS rata_rata
        FROM (SELECT
        DATE_TRUNC('month',time)AS  month,
        COUNT(id) AS total_siswa,
        SUM(nilai) AS total_nilai
        FROM nilai
        GROUP BY DATE_TRUNC('month',time)
        ORDER BY DATE_TRUNC('month',time) ASC) as rekap
        """

    # def init(self):
    #     self.env.cr.execute(self._query())
    
    def init(self):
        self.env.cr.execute(
            """CREATE OR REPLACE VIEW %s as (%s)""" % (
                self._table, self._query())
        )