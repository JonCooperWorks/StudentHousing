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

