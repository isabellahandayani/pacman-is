{
    "name": "pacman-is",
    "author": "Pacman",
    "version": "13.0.1.0.0",
    "category": "education",
    "summary": "Sistem Informasi Basis Data Siswa Pacmann",
    "descriptsion": "Sistem Informasi Basis Data Siswa Pacmann",
    "website": "",
    "depends": ["web", "base", "website"],
    "data": [
        'security/ir.model.access.csv',
        'views/rekap_modul.xml',
        'views/siswa_CRUD.xml',
        'views/add_siswa.xml',
        'views/update_siswa.xml',
    ],
    "installable": True,
    "application": True,
    "license": "OEEL-1"
}