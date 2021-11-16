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