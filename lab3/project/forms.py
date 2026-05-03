from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, ValidationError


class TourOperatorForm(FlaskForm):
    class Meta:
        csrf = False
    name = SelectField(
        'Tour Operator Name',
        choices=[],
        validators=[
            DataRequired(message="Please select a name"),
            Length(message="Please chose a valid name", min=1, max=75)
        ]
    )
    submit = SubmitField('Submit')

class DaysNumberForm(FlaskForm):
    class Meta:
        csrf = False
    days = IntegerField('Number of days', validators=[
        DataRequired(message="Please select a valid days number from 1 to 10000"),
        NumberRange(min=1, max=10000)
    ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    class Meta:
        csrf = False
    search_option = RadioField('Search Option', 
        choices=[
            ('tour_operator', 'By Tour Operator'),
            ('days', 'By Tour Duration'),
            ('luxury', 'Best tour to Turkey'),
        ],
        validators=[DataRequired(message="Please select an option")]
    )
    name = SelectField(
        'Tour Operator Name',
        choices=[],
        validators=[]
    )
    days = IntegerField('Number of days', validators=[])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if self.search_option.data == 'tour_operator' and not field.data:
            raise ValidationError('Name is required to search by tour operator.')
        
    def validate_days(self, field):
        if self.search_option.data == 'days':
            if not field.data:
                raise ValidationError('Number of days is required to filter by tour duration.')
            
            NumberRange(
                min=1, max=10000,
                message="Please select a valid days number from 1 to 10000"
            )(self, field)
        else:
            Optional()(self, field)


class TourForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired(), Length(min=1, max=75)])
    tour_operator = StringField('Tour operator', validators=[DataRequired(), Length(min=1, max=75)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, max=100000)])
    days = IntegerField('Duration in days', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = SubmitField('Create Tour')