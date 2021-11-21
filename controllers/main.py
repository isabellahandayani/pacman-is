from odoo import http
from odoo.http import request


class RekapModul(http.Controller):
    @http.route("/rekap", auth="public", website=True)
    def rekap_modul(self, **kw):

        rekap_modul = request.env["rekap.modul"].sudo().search([])
        rekap_summary = request.env["rekap.summary"].sudo().search([])

        data = {"rekap_modul": rekap_modul, "rekap_summary": rekap_summary}

        return request.render("pacman-is.rekap_modul_page", data)


class SiswaCRUD(http.Controller):
    @http.route("/siswa", auth="public", website=True)
    def siswa_CRUD(self, **kw):
        siswa = request.env["siswa"].sudo().search([])
        data = {"data_siswa": siswa}

        return request.render("pacman-is.siswa_crud_page", data)

    @http.route("/siswa/addsiswa", auth="public", website=True)
    def addSiswaPage(self, **kw):
        return request.render("pacman-is.add_siswa_page", {})

    @http.route("/siswa/addsiswa/submit", auth="public", website=True)
    def addSiswa(self, **post):
        data_siswa = (
            request.env["siswa"]
            .sudo()
            .create(
                {
                    "nama": post.get("nama"),
                    "email": post.get("email"),
                    "work": post.get("pekerjaan"),
                    "education": post.get("pendidikan"),
                    "usia": post.get("usia"),
                    "batch": post.get("batch"),
                }
            )
        )

        return request.redirect("/siswa")

    @http.route("/siswa/deletesiswa", auth="public", website=True)
    def deleteSiswa(self, **post):
        request.env["siswa"].sudo().search([("id", "=", post.get("del-ID"))]).unlink()
        return request.redirect("/siswa")

    @http.route("/siswa/updatesiswa", auth="public", website=True)
    def updateSiswaPage(self, **post):
        data_siswa = (
            request.env["siswa"].sudo().search([("id", "=", post.get("upd-ID"))])
        )
        data = {"data_siswa": data_siswa}
        return request.render("pacman-is.update_siswa_page", data)

    @http.route("/siswa/updatesiswa/submit", auth="public", website=True)
    def updateSiswa(self, **post):
        data_siswa = (
            request.env["siswa"].sudo().search([("id", "=", post.get("upd-ID"))])
        )
        for record in data_siswa:
            if post.get("nama") != "":
                record.write(
                    {
                        "nama": post.get("nama"),
                    }
                )
            if post.get("email") != "":
                record.write(
                    {
                        "email": post.get("email"),
                    }
                )
            if post.get("pekerjaan") != "":
                record.write(
                    {
                        "pekerjaan": post.get("pekerjaan"),
                    }
                )
            if post.get("pendidikan") != "":
                record.write(
                    {
                        "pendidikan": post.get("pendidikan"),
                    }
                )
            if post.get("usia") != "":
                record.write(
                    {
                        "usia": post.get("usia"),
                    }
                )
            if post.get("batch") != "":
                record.write(
                    {
                        "batch": post.get("batch"),
                    }
                )
        return request.redirect("/siswa")

    @http.route("/overview", auth="public", website=True)
    def overview_siswa(self, **kw):
        siswa = request.env["siswa"].sudo().search([])
        filter_count = 0
        count = request.env["siswa"].sudo().search_count([])
        data = {"siswa": siswa, "filter_count": filter_count, "count": count}
        return request.render("pacman-is.overview_siswa", data)

    @http.route("/laporan", auth="public", website=True)
    def generate_report(self, **kw):
        laporan = request.env["rekap.siswa"].sudo().search([])
        data = {"month": laporan}
        # return request.render("pacman-is.generate_report", data)
        return request.render("pacman-is.laporan_graph_view", data)
        # return "laporan"

    @http.route("/filter-overview", auth="public", website=True)
    def filter_overview(self, **post):
        # Getting filters
        educations = [post.get("ed1"), post.get("ed2"), post.get("ed3")]
        works = [post.get("work1"), post.get("work2"), post.get("work3")]
        ages = [post.get("age1"), post.get("age2"), post.get("age3")]

        # Filtering none values
        educations = [education for education in educations if education]
        works = [work for work in works if work]
        ages = [age for age in ages if age]

        # Creating search domains
        search_domain = []
        if educations:
            education_domain = ("education", "in", educations)
            search_domain.append(education_domain)

        if works:
            if "All Jobs" not in works:
                work_domain = ("work", "in", works)
                search_domain.append(work_domain)

        age_domain = []
        for age in ages:
            if age == "16-20":
                domain = [("usia", ">=", 16), ("usia", "<=", 20)]
                age_domain.extend(domain)
            if age == "21-27":
                domain = [("usia", ">=", 21), ("usia", "<=", 27)]
                if age_domain:
                    age_domain.insert(0, "|")
                    age_domain.insert(1, "&")
                    domain.insert(0, "&")
                age_domain.extend(domain)
            if age == "> 27":
                if len(age_domain) == 2:
                    age_domain.insert(0, "|")
                    age_domain.insert(1, "&")
                elif len(age_domain) > 2:
                    age_domain.insert(0, "|")
                domain = ("usia", ">", 27)
                age_domain.append(domain)
        if age_domain:
            search_domain.extend(age_domain)

        # Filtering the data with the search domain
        siswa = request.env["siswa"].sudo().search(search_domain)
        count = request.env["siswa"].sudo().search_count([])
        filter_count = request.env["siswa"].sudo().search_count(search_domain)
        data = {
            "siswa": siswa,
            "filter_count": filter_count,
            "count": count,
        }
        return request.render("pacman-is.overview_siswa", data)
