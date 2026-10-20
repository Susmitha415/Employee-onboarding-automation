def populate_template(template_text, employee):
    content = template_text

    employee_data = employee.to_dict()

    for key, value in employee_data.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(
            placeholder, str(value)
        )

    return content