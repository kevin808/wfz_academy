# -*- coding: utf-8 -*-

from odoo import fields, models

class Person(models.Model):
    _name = 'res.person'

    name = fields.Char("Name", required=True)

    active = fields.Boolean(default=True)

    image = fields.Binary(attachment=True, string="Photo")

    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)