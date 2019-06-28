# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class academy(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats", required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()
    instructor_id = fields.Many2one('res.person', string="Instructor",
                                    domain=[('instructor', '=', True)])
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.person', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", compute='_set_end_date')
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats

    # 视图里面没有添加hours，所以以下两个方法运行时并不会主动调用
    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('duration', 'start_date')
    def _set_end_date(self):
        tmp = self.duration
        if tmp != round(tmp):
            # 这里加0.5，使得天数不为整数时，天数始终能加一
            tmp = tmp + 0.5
        self.end_date = datetime.datetime.strptime(
            self.start_date, "%Y-%m-%d") + datetime.timedelta(days=round(tmp))

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError(
                _("A session's instructor can't be an attendee"))

    @api.one
    @api.constrains('seats', 'attendee_ids')
    def _check_seats_and_attendees(self):
        if self.seats < 0:
            raise exceptions.ValidationError(
                _("The number of available seats may not be negative"))
        if self.seats < len(self.attendee_ids):
            raise exceptions.ValidationError(
                _("Increase seats or remove excess attendees"))
