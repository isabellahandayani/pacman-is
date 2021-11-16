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