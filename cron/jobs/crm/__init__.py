from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime, timezone
from datetime import date
from controllers.mailing.templates.default_template import Default_Template
from controllers.mailing import Mailing
from datetime import datetime, time, timezone
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class CRM_Background_Jobs:
    def __init__(self, dbms=None, tc=None) -> None:
        self.dbms = dbms
        self.tc = tc
        self.mailing = Mailing(dbms=dbms, tc=None)
    def escalate_ticket(self):
        pp("test bg")
        date_time = datetime.today()
        current_date = date_time.date()
        current_day = date_time.strftime('%A')
        current_time = datetime.now(timezone.utc).time()  
        try:
            tickets = self.tickets()
            if tickets:
                for tic in tickets:
                    customer = tic['customer']
                    sla_data = self.sla(customer=customer)
                    if not sla_data:
                        continue
                    
                    sla_start_date = sla_data.get('start_date', None)
                    sla_end_date = sla_data.get('end_date', None)
                    working_hours = sla_data.get('working_hours', None)
                    sla_priority = sla_data.get('sla_priorities', None)
                    
                    if sla_start_date and sla_end_date:
                        if isinstance(sla_start_date, str):
                            sla_start_date = datetime.strptime(sla_start_date, '%Y-%m-%d').date()
                        if isinstance(sla_end_date, str):
                            sla_end_date = datetime.strptime(sla_end_date, '%Y-%m-%d').date()

                        if sla_start_date <= current_date <= sla_end_date:
                            if working_hours:
                               for wh in working_hours:
                                    if wh['day'] == current_day:
                                        start_time = datetime.strptime(wh['start_time'], '%H:%M').time()
                                        end_time = datetime.strptime(wh['end_time'], '%H:%M').time()

                                        if start_time <= current_time <= end_time:
                                            for sla_p in sla_priority:
                                                sla_prior = sla_p['priority']
                                                if tic['priority'] == sla_prior:
                                                    first_response = sla_p['first_response_time']
                                                    ticket_creation_time = tic['creation_time']

                                                    if not isinstance(ticket_creation_time, str):
                                                        ticket_creation_time = str(ticket_creation_time)
                                                    ticket_age = datetime.fromisoformat(ticket_creation_time).replace(tzinfo=None)
                                                    current_date_time = datetime.now()
                                                    time_diff = current_date_time - ticket_age
                                                    hours = time_diff.total_seconds() // 3600
                                                    minutes = (time_diff.total_seconds() % 3600) // 60
                                                    first_response_hours, first_response_minutes = map(int, first_response.split(":"))
                                                    first_response_total_minutes = first_response_hours * 60 + first_response_minutes
                                                    ticket_age_total_minutes = hours * 60 + minutes

                                                    if ticket_age_total_minutes > first_response_total_minutes:
                                                        escalation_matrix = self.get_escalation_metrix()
                                                        for metrix in escalation_matrix:
                                                            if metrix.get('customer') == customer and metrix.get('current_priority') == tic['priority']:
                                                                receiver = metrix.get('escalate_to')
                                                                subj = tic.get('subject', 'No Subject')  
                                                                description = tic.get('description', 'No Description')  
                                                                if receiver: 
                                                                    content = f"""
                                                                            <head>
                                                                                <style>
                                                                                    body {{
                                                                                        font-family: Arial, sans-serif;
                                                                                        font-size: 1em;
                                                                                        line-height: 1.5;
                                                                                        color: #333;
                                                                                    }}
                                                                                    .container {{
                                                                                        padding: 20px;
                                                                                        background-color: #f9f9f9;
                                                                                        border-radius: 10px;
                                                                                        max-width: 600px;
                                                                                        margin: auto;
                                                                                    }}
                                                                                    .btn {{
                                                                                        text-decoration: none;
                                                                                        background-color: #151030;
                                                                                        color: white !important;
                                                                                        border-radius: 10px;
                                                                                        padding: 15px 30px;
                                                                                        display: inline-block;
                                                                                    }}
                                                                                    .code {{
                                                                                        font-size: 30px;
                                                                                        font-weight: bold;
                                                                                        margin-top: 10px;
                                                                                    }}
                                                                                </style>
                                                                            </head>
                                                                            <body>
                                                                                <div class="container">
                                                                                    <h2>Hello {receiver}!</h2>
                                                                                    <p>A ticket from {customer} has been escalated to you for urgent resolution. See the details below:</p>
                                                                                    <h3>Ticket Details:</h3>
                                                                                    <p><strong>Subject:</strong> {subj}</p>
                                                                                    <p><strong>Hours Passed:</strong> {hours} hours</p>
                                                                                    <p><strong>Description:</strong> {description}</p>
                                                                                    <p>To proceed with the resolution, please refer to the link below:</p>
                                                                                    <div style="margin:30px 0">
                                                                                        <a href="https://hrmis.exams-council.org.zm/ticket/" class="btn">View Ticket</a>
                                                                                    </div>
                                                                                    <p>Alternatively, you can go to the following link:</p>
                                                                                    <a href="https://hrmis.exams-council.org.zm/ticket/">https://hrmis.exams-council.org.zm/ticket/</a>
                                                                                </div>
                                                                            </body>
                                                                            </html>
                                                                        """
                                                                    try:
                                                                        self.mailing.send_mail(recipient=receiver,subject=subj,body=Default_Template.template(content, "Ticket Escalation Notification"))
                                                                        pp(f"Email sent successfully to {receiver}")
                                                                        tic['doc_status'] = "Ticket Escalated"
                                                                        update = self.dbms.update("Ticket", tic, privilege=True, skip_hooks=True, skip_audit_trail=True)
                                                                    except Exception as email_error:
                                                                        pp(f"Failed to send email to {receiver}: {email_error}")
                                                                else:
                                                                    pp(f"Missing recipient email for escalation: {tic}")
                            else:
                                pp(f"Working hours are missing for customer {customer}.")
            else:
                pp("No tickets fetched.")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    def get_escalation_metrix(self):
        try:
            escalation_rules = self.dbms.get_list("Escalation_Rule", privilege=True, fetch_linked_tables=True)
            if escalation_rules:
                rules_data = escalation_rules['data']['rows']
                processed_rules = []  
                for rule in rules_data:
                    actions = rule.get('escalation_actions', [])
                    for action in actions:
                        processed_rules.append({ "customer": rule.get("customer"), "ticket_type": action.get("ticket_type"),
                            "current_priority": action.get("current_priority"), "next_priority": action.get("next_priority"),
                            "escalate_to": action.get("escalate_to"), "created_on": rule.get("created_on"), "creation_time": rule.get("creation_time"),
                        })
                return processed_rules  
            else:
                return []  
        except Exception as e:
            print(f"Exception occurred while fetching escalation matrix: {str(e)}")
            return []

    def tickets(self):
        try:
            get_ticket = self.dbms.get_list("Ticket", privilege=True, filters={"status": "Open"})
            if get_ticket.status == utils.ok:
                ticket_data = get_ticket['data']['rows']
                escalation_data = []
                for ticket in ticket_data:
                    ticket_info = {"id": ticket['id'], 'subject': ticket['subject'],  "docstatus": ticket['docstatus'], "status": ticket['status'], "description": ticket['description'], 'customer': ticket['customer'],'priority': ticket['priority'],
                        'status': ticket['status'],'creation_time': ticket['creation_time'],'relation_manager': ticket['relation_manager'],'ticket_type': ticket['ticket_type'] }
                    escalation_data.append(ticket_info)
                return escalation_data
            else:
                pp(f"Failed to fetch ticket data. Status: {get_ticket.status}")
                return None
        except Exception as e:
            print(f"Error in tickets method: {str(e)}")
            return None

    def sla(self, customer):
        try:
            sla = self.dbms.get_list("Service_Level_Agreement", privilege=True, fetch_linked_tables=True)
            if sla.status == utils.ok:
                sla_rows = sla["data"]["rows"]
                sla_data = {} 
                for sla_item in sla_rows:
                    sla_name = sla_item['name']  
                    sla_priorities = sla_item['sla_priority']
                    working_hrs = sla_item['working_hours']
                    customer_name = sla_item['customer']
                    start_date = sla_item['start_date']
                    end_date = sla_item['end_date']   
                    if customer_name == customer:
                        sla_info = { 'customer': customer_name,  'start_date': start_date,  'end_date': end_date,  'sla_priorities': [], 'working_hours': []}
                        for priority_item in sla_priorities:
                            priority = priority_item['priority']
                            first_response_time = priority_item['first_response_time']
                            resolution_time = priority_item['resolution_time']
                            
                            sla_info['sla_priorities'].append({'priority': priority,'first_response_time': first_response_time,'resolution_time': resolution_time})
                        sla_info['working_hours'] = [{'day': wh['day'], 'start_time': wh['start_time'], 'end_time': wh['end_time']} for wh in working_hrs]
                        
                        sla_data[customer_name] = sla_info
                return sla_data.get(customer, None) 
            
            else:
                raise Exception("Failed to fetch SLA data.")
        
        except Exception as e:
            raise Exception(f"An error occurred in SLA method: {str(e)}")
    def contract_service(self):
        get_contract = self.dbms.get_list("Contract", privilege=True)
    @classmethod
    def ticket_escalation(cls, dbms, tc=None):
        instance = cls(dbms, tc)
        return instance.escalate_ticket()