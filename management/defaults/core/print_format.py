print_format = {
    "model":"Print_Format",
    "data":[
        {
            "name":"Payslip Standard Format",
            "app_model":"Payslip",
            "is_default":1,
            "html": """
                <!DOCTYPE html>
                <html lang='en'>
                    <head>
                        <meta charset='UTF-8'>
                        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                        <title>{{ name }}</title>
                        <link rel='stylesheet' href='/static/css/print_layout.css'>
                        <script src='/static/js/tailwindcss.js'></script>
                        <style>
                            @media print {
                                body { font-size: 12px }
                            }
                        </style>
                    </head>
                    <body class='bg-white text-gray-800'>
                        <div class='w-[800px] mx-auto p-6'>
                            <!-- HEADER
                            <div class='flex justify-between items-start border-b pb-4 mb-4'>
                                <div>
                                    <h1 class='text-xl font-bold'>{{ linked_fields.company.company_name }}</h1>
                                    <p class='text-xs'>{{ linked_fields.company.address }}</p>
                                    <p class='text-xs'>Phone: {{ linked_fields.company.phone }}</p>
                                    <p class='text-xs'>Email: {{ linked_fields.company.email }}</p>
                                </div>
                                <h2 class='text-2xl font-bold tracking-wide'>PAYSLIP</h2>
                            </div> -->

                            <div class='flex justify-between items-start border-b pb-4 mb-4'>
                                <!-- COMPANY BLOCK -->
                                <div class='flex flex-col gap-2'>
                                    <!-- LOGO -->
                                    {% if linked_fields.company.company_logo %}
                                        <img
                                            src='http://{{ full_url }}/{{ linked_fields.company.company_logo }}'
                                            alt='Company Logo'
                                            class='h-16 object-contain'
                                        >
                                    {% endif %}

                                    <!-- COMPANY DETAILS -->
                                    <div>
                                        <h1 class='text-xl font-bold'>
                                            {{ linked_fields.company.company_name }}
                                        </h1>
                                        <p class='text-xs'>{{ linked_fields.company.address }}</p>
                                        <p class='text-xs'>Phone: {{ linked_fields.company.phone }}</p>
                                        <p class='text-xs'>Email: {{ linked_fields.company.email }}</p>
                                    </div>
                                </div>

                                <!-- DOCUMENT TITLE -->
                                <h2 class='text-2xl font-bold tracking-wide self-start'>
                                    PAYSLIP
                                </h2>
                            </div>

                            <!-- INFO SECTION -->
                            <div class='grid grid-cols-2 gap-6 mb-6'>

                                <!-- EMPLOYEE INFO -->
                                <div>
                                    <div class='bg-blue-200 text-xs font-bold px-2 py-1 mb-2'>
                                        EMPLOYEE INFORMATION
                                    </div>
                                    <p><b>Full Name:</b> {{ employee_names }}</p>
                                    <p>{{ linked_fields.employee.address }}</p>
                                    <p>Phone: {{ linked_fields.employee.phone }}</p>
                                    <p>Email: {{ linked_fields.employee.email }}</p>
                                </div>

                                <!-- PAY INFO -->
                                <div class='grid grid-cols-3 text-xs border'>
                                    <div class='p-2 bg-blue-100 font-bold'>PAY DATE</div>
                                    <div class='p-2 bg-blue-100 font-bold'>PAY TYPE</div>
                                    <div class='p-2 bg-blue-100 font-bold'>PERIOD</div>

                                    <div class='p-2'>{{ to_date }}</div>
                                    <div class='p-2'>Monthly</div>
                                    <div class='p-2'>{{ period }}</div>

                                    <div class='p-2 bg-blue-100 font-bold'>PAYROLL #</div>
                                    <div class='p-2 bg-blue-100 font-bold'>NAPS A NO</div>
                                    <div class='p-2 bg-blue-100 font-bold'>TPIN</div>

                                    <div class='p-2'>{{ name }}</div>
                                    <div class='p-2'>{{ linked_fields.employee.napsa }}</div>
                                    <div class='p-2'>{{ tax_identification_no }}</div>
                                </div>
                            </div>

                            <!-- EARNINGS TABLE -->
                            <table class='w-full border text-xs mb-6'>
                                <thead class='bg-gray-200'>
                                    <tr>
                                        <th class='text-left p-2'>EARNINGS</th>
                                        <th class='text-right p-2'>HOURS</th>
                                        <th class='text-right p-2'>RATE</th>
                                        <th class='text-right p-2'>CURRENT</th>
                                        <th class='text-right p-2'>YTD</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for earning in earnings %}
                                    <tr class='border-t'>
                                        <td class='p-2'>{{ earning.earning }}</td>
                                        <td class='p-2 text-right'>{{ earning.hours or '-' }}</td>
                                        <td class='p-2 text-right'>{{ earning.rate or '-' }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(earning.amount) }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(earning.ytd or earning.amount) }}</td>
                                    </tr>
                                    {% endfor %}

                                    <tr class='bg-gray-200 font-bold border-t'>
                                        <td colspan='3' class='p-2 text-right'>GROSS PAY</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(gross) }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(ytd_gross) }}</td>
                                    </tr>
                                </tbody>
                            </table>

                            <!-- DEDUCTIONS -->
                            <table class='w-full border text-xs mb-6'>
                                <thead class='bg-gray-200'>
                                    <tr>
                                        <th class='text-left p-2'>DEDUCTIONS</th>
                                        <th class='text-right p-2'>CURRENT</th>
                                        <th class='text-right p-2'>YTD</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for deduction in deductions %}
                                    <tr class='border-t'>
                                        <td class='p-2'>{{ deduction.deduction }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(deduction.amount) }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(deduction.ytd or deduction.amount) }}</td>
                                    </tr>
                                    {% endfor %}

                                    <tr class='bg-gray-200 font-bold border-t'>
                                        <td class='p-2 text-right'>TOTAL DEDUCTIONS</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(total_deductions) }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(ytd_deductions) }}</td>
                                    </tr>
                                </tbody>
                            </table>

                            <!-- NET PAY -->
                            <div class='flex justify-end'>
                                <table class='w-1/2 border text-xs'>
                                    <tr class='bg-gray-300 font-bold'>
                                        <td class='p-2 text-right'>NET PAY</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(net) }}</td>
                                        <td class='p-2 text-right'>{{ utils.thousand_separator(ytd_net) }}</td>
                                    </tr>
                                </table>
                            </div>

                            <!-- FOOTER -->
                            <div class='text-center text-xs mt-6'>
                                If you have any questions about this payslip, please contact:<br>
                                {{ linked_fields.company.email }}
                            </div>
                        </div>
                    </body>
                </html>
            """
        },
        
        {
            "name":"Employee Promotion Letter",
            "app_model":"Employee_Promotion",
            "is_default":1,
            "html": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <title>Employee Promotion Letter</title>
                <style>
                    body {
                    font-family: "Segoe UI", Arial, sans-serif;
                    background-color: #f3f4f6;
                    margin: 0;
                    padding: 40px;
                    color: #111827;
                    }

                    .document {
                    max-width: 820px;
                    margin: auto;
                    background-color: #ffffff;
                    padding: 50px;
                    border: 1px solid #e5e7eb;
                    }

                    .header {
                    border-bottom: 3px solid #0f172a;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                    }

                    .header h1 {
                    margin: 0;
                    font-size: 22px;
                    font-weight: 600;
                    color: #0f172a;
                    }

                    .meta {
                    margin-top: 10px;
                    font-size: 14px;
                    }

                    .content p {
                    line-height: 1.8;
                    margin-bottom: 18px;
                    font-size: 15px;
                    }

                    .signature {
                    margin-top: 50px;
                    }

                    .signature strong {
                    display: block;
                    margin-top: 12px;
                    }

                    .acknowledgement {
                    margin-top: 50px;
                    font-size: 14px;
                    color: #374151;
                    }
                </style>
                </head>
                <body>

                <div class="document">
                    <div class="header">
                    <h1>Promotion Letter</h1>
                    <div class="meta">
                        <strong>Date:</strong> {{ approved_on or '-'}}
                    </div>
                    </div>

                    <div class="content">
                    <p>
                        To:<br>
                        <strong>{{ employee_name }}</strong><br>
                        {{ current_designation }}<br>
                        {{ department }}
                    </p>

                    <p>Dear <strong>{{ employee_name }}</strong>,</p>

                    <p>
                        Following a formal review process and in recognition of your performance, experience, and
                        contribution to the organization, we are pleased to confirm your promotion to the position of
                        <strong>{{ revised_designation }}</strong>, effective <strong>{{ effective_date }}</strong>.
                    </p>

                    <p>
                        This promotion reflects the organization’s confidence in your ability to undertake increased
                        responsibilities and to support its strategic and operational objectives.
                    </p>

                    <p>
                        Any adjustments to your terms of employment, including remuneration and benefits, shall be
                        implemented in accordance with established company policies.
                    </p>

                    <p>
                        We congratulate you on this appointment and trust that you will continue to uphold the
                        organization’s standards of excellence and professionalism.
                    </p>

                    <div class="signature">
                        Yours faithfully,
                        <strong>[Authorizing Officer’s Name]</strong>
                        [Job Title]<br>
                        {{ company }}
                    </div>

                    <div class="acknowledgement">
                        <p>
                        Acknowledged and Accepted by:<br><br>
                        _______________________________<br>
                        {{ employee_name }} & _________________________________
                        </p>
                    </div>
                    </div>
                </div>

                </body>
                </html>
                """
        },
        {
            "name":"Appointment Letter",
            "app_model":"Employee",
            "is_default":1,
            "html": """
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Appointment Letter</title>
                        <style>
                            body {
                            font-family: "Segoe UI", Arial, sans-serif;
                            background-color: #f3f4f6;
                            margin: 0;
                            padding: 40px;
                            color: #111827;
                            }

                            .letter {
                            max-width: 820px;
                            margin: auto;
                            background-color: #ffffff;
                            padding: 50px;
                            border: 1px solid #e5e7eb;
                            }

                            .header {
                            border-bottom: 3px solid #0f172a;
                            padding-bottom: 20px;
                            margin-bottom: 30px;
                            }

                            .header h1 {
                            margin: 0;
                            font-size: 22px;
                            font-weight: 600;
                            color: #0f172a;
                            }

                            .meta {
                            margin-top: 10px;
                            font-size: 14px;
                            }

                            .content p {
                            line-height: 1.8;
                            margin-bottom: 18px;
                            font-size: 15px;
                            }

                            .signature {
                            margin-top: 50px;
                            }

                            .signature strong {
                            display: block;
                            margin-top: 12px;
                            }

                            .acknowledgement {
                            margin-top: 50px;
                            font-size: 14px;
                            color: #374151;
                            }
                        </style>
                    </head>
                    <body>

                        <div class="letter">
                            <div class="header">
                                <h1>Appointment Letter</h1>
                                <div class="meta">
                                    <strong>Date:</strong> [Insert Date]
                                </div>
                            </div>

                            <div class="content">
                                <p>
                                    To:<br>
                                    <strong>[Employee Name]</strong><br>
                                    [Address or Department]
                                </p>

                                <p>Dear <strong>[Employee Name]</strong>,</p>

                                <p>
                                    We are pleased to offer you an appointment to the position of
                                    <strong>[Job Title]</strong> with <strong>[Company Name]</strong>,
                                    effective <strong>[Commencement Date]</strong>.
                                </p>

                                <p>
                                    You will be assigned duties and responsibilities consistent with your role
                                    and as directed by management. You shall report to
                                    <strong>[Supervisor / Department]</strong>.
                                </p>

                                <p>
                                    Your employment shall be subject to the organization’s policies, procedures,
                                    and terms and conditions of service, including confidentiality and code of
                                    conduct requirements.
                                </p>

                                <p>
                                    We trust that you will discharge your duties diligently and uphold the
                                    organization’s standards of professionalism and integrity.
                                </p>

                                <div class="signature">
                                    Yours faithfully,
                                    <strong>[Authorizing Officer’s Name]</strong>
                                    [Job Title]<br>
                                    [Company Name]
                                </div>

                                <div class="acknowledgement">
                                    <p>
                                        Accepted by:<br><br>
                                        _______________________________<br>
                                        Employee Name & Signature<br>
                                        Date
                                    </p>
                                </div>
                            </div>
                        </div>
                    </body>
                </html>
            """
        },
        {
            "name":"Transfer Latter Letter",
            "app_model":"Employee_Transfer_Request",
            "is_default":1,
            "html": """
                <!DOCTYPE html>
                <html lang='en'>
                    <head>
                        <meta charset='UTF-8'>
                        <title>Employee Transfer Letter</title>
                        <style>
                            body {
                            font-family: 'Segoe UI', Arial, sans-serif;
                            background-color: #f3f4f6;
                            margin: 0;
                            padding: 40px;
                            color: #111827;
                            }

                            .letter {
                            max-width: 820px;
                            margin: auto;
                            background-color: #ffffff;
                            padding: 50px;
                            border: 1px solid #e5e7eb;
                            }

                            .header {
                            border-bottom: 3px solid #0f172a;
                            padding-bottom: 20px;
                            margin-bottom: 30px;
                            }

                            .header h1 {
                            margin: 0;
                            font-size: 22px;
                            font-weight: 600;
                            color: #0f172a;
                            }

                            .meta {
                            margin-top: 10px;
                            font-size: 14px;
                            }

                            .content p {
                            line-height: 1.8;
                            margin-bottom: 18px;
                            font-size: 15px;
                            }

                            .signature {
                            margin-top: 50px;
                            }

                            .signature strong {
                            display: block;
                            margin-top: 12px;
                            }

                            .acknowledgement {
                            margin-top: 50px;
                            font-size: 14px;
                            color: #374151;
                            }
                        </style>
                    </head>
                    <body>
                        <div class='letter'>
                            <div class='header'>
                                <h1>Employee Transfer Letter</h1>
                                <div class='meta'>
                                    <strong>Date:</strong> {{ transfer_date or '-'}}
                                </div>
                            </div>

                            <div class='content'>
                                <p>
                                    To:<br>
                                    <strong>{{ transfer_employee_name }}</strong><br>
                                    [Current Department / Location]
                                </p>

                                <p>Dear <strong>{{ transfer_employee_name }}</strong>,</p>
                                <p>
                                    This letter serves to formally notify you that management has approved your transfer from
                                    the <strong>{{ transfer_employee_department }}</strong> to the
                                    <strong>{{ new_location }}</strong>, effective
                                    <strong>{{ transfer_date }}</strong>.
                                </p>

                                <p>
                                    The transfer is made in accordance with organizational requirements and does not affect
                                    your existing terms and conditions of service unless otherwise communicated.
                                </p>

                                <p>
                                    Upon transfer, you will report to <strong>[New Supervisor / Department Head]</strong>.
                                    You are required to complete all handover procedures prior to the effective date.
                                </p>

                                <p>
                                    Management trusts in your continued professionalism and cooperation.
                                </p>

                                <div class='signature'>
                                    Yours faithfully,
                                    <strong>{{' - '}}</strong>
                                    [Job Title]<br>
                                    {{ ' - ' }}
                                </div>

                                <div class='acknowledgement'>
                                    <p>
                                        Acknowledged by:<br><br>
                                        _______________________________<br>
                                        {{ employee_name }} & Signature<br>
                                        Date {{ transfer_date }}
                                    </p>
                                </div>
                            </div>
                        </div>

                    </body>
                </html>
            """
        }
    ]
}