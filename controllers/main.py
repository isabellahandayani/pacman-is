from odoo import http
from odoo.http import request


class RekapModul(http.Controller):
    @http.route('/rekap', auth='public', website=True)
    def rekap_modul(self, **kw):

        rekap_modul = request.env['rekap.modul'].sudo().search([])
        rekap_summary = request.env['rekap.summary'].sudo().search([])


        data = {
            'rekap_modul': rekap_modul,
            'rekap_summary': rekap_summary
        }

        return request.render('pacman-is.rekap_modul_page', data)

class SiswaCRUD(http.Controller):
    @http.route('/siswa', auth='public', website=True)
    def siswa_CRUD(self, **kw):
        siswa = request.env['siswa'].sudo().search([])
        data = {
            'teachers': siswa
        }

        return request.render('pacman-is.siswa_crud_page', data)
    
    @http.route('/siswa/addsiswa', auth='public', website=True)
    def addSiswaPage(self, **kw):
        return request.render('pacman-is.add_siswa_page', {})

    @http.route('/siswa/addsiswa/submit', auth='public', website=True)
    def addSiswa(self, **post):
        data_siswa = request.env['siswa'].sudo().create({
            'nama' : post.get('nama'),
            'email' : post.get('email'),
            'work' : post.get('pekerjaan'),
            'education' : post.get('pendidikan'),
            'usia' : post.get('usia'),
            'batch' : post.get('batch')
        })
        
        return request.redirect('/siswa')