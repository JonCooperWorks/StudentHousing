from jinja2 import evalcontextfilter, Markup, escape

@evalcontextfilter
def bv2yn(eval_ctx, value):
    if value:
        result = "Yes"
    else:
        result = "No"
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

@evalcontextfilter    
def int2parish(eval_ctx, value):
    parish_dict = dict(parishes)
    return parish_dict[value]
    
@evalcontextfilter
def int2occupancy(eval_ctx, value):
    occupancy_dict = dict(occupancies)
    if eval_ctx.autoescape:
        return Markup(occupancy_dict[value])
    return occupancy_dict[value]

@evalcontextfilter
def to_phone_number(eval_ctx, value):
    #Start by ensuring string has 10 digits
    digits = filter(lambda x: x.isdigit(),value)
    if len(digits) == 10:
        phone_number = '('+ digits[0:3] + ')' + digits[3:6] + '-' + digits[6:]
    else:
        phone_number = digits[0:3] +'-' + digits[3:]
    if eval_ctx.autoescape:
        return Markup(phone_number)
    return phone_number

#List of parishes for form
parishes = [
    (1, "Kingston"),
    (2, "St. Andrew"),
    (3, "St. Catherine"),
    (4, "Clarendon"),
    (5, "Manchester"),
    (6, "St. Elizabeth"),
    (7, "Westmoreland"),
    (8, "Hanover"),
    (9, "St. James"),
    (10, "Trelawny"),
    (11, "St. Ann"),
    (12, "St. Mary"),
    (13, "Portland"),
    (14, "St. Thomas")
]

occupancies = [
    (1, 'Single'), 
    (2, 'Double'), 
    (3, 'Triple'), 
    (4, 'Multiple')
]