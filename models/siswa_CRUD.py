from odoo import models, fields

class read_siswa(models.Model):
    _name = 'read.siswa'
    _auto = False
    _description = 'Data Siswa'

    id_siswa = fields.Integer(string="ID Siswa", required=True)
    batch = fields.Integer(string="Batch", required=True)
    nama = fields.Char(size=255, string="Nama", required=True)
    email = fields.Char(size=255, string="Email", required=True)
    work = fields.Char(size=255, string="Pekerjaan", required=True)
    education = fields.Char(size=255, string="Pendidikkan Terakhir", required=True)
    usia = fields.Integer(string="Usia", required=True)

    def _query(self):
        return """
        SELECT *
        FROM siswa
        """

    def init(self):
        self.env.cr.execute(self._query())