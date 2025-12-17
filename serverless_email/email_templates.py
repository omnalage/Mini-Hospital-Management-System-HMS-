def appointment_confirmation_template(patient_name, doctor_name, appointment_date, start_time, end_time='', specialization=''):
    """Generate HTML for appointment confirmation email"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .details {{ line-height: 1.8; }}
                .footer {{ margin-top: 20px; text-align: center; color: #999; font-size: 12px; }}
                .button {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Appointment Confirmed!</h1>
                </div>
                
                <div class="content">
                    <p>Dear <strong>{patient_name}</strong>,</p>
                    
                    <p>Your appointment has been successfully scheduled. Here are the details:</p>
                    
                    <div class="details">
                        <p><strong>Doctor:</strong> {doctor_name}</p>
                        {f'<p><strong>Specialization:</strong> {specialization}</p>' if specialization else ''}
                        <p><strong>Date:</strong> {appointment_date}</p>
                        <p><strong>Time:</strong> {start_time}{f" - {end_time}" if end_time else ""}</p>
                    </div>
                    
                    <p>Please arrive 10 minutes early to complete any necessary paperwork.</p>
                    
                    <p>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</p>
                    
                    <a href="http://localhost:3000/appointments" class="button">View Appointment</a>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 Hospital Management System. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """


def appointment_reminder_template(patient_name, doctor_name, appointment_date, start_time):
    """Generate HTML for appointment reminder email"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .details {{ line-height: 1.8; }}
                .footer {{ margin-top: 20px; text-align: center; color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Appointment Reminder</h1>
                </div>
                
                <div class="content">
                    <p>Hello <strong>{patient_name}</strong>,</p>
                    
                    <p>This is a reminder about your upcoming appointment:</p>
                    
                    <div class="details">
                        <p><strong>Doctor:</strong> {doctor_name}</p>
                        <p><strong>Date:</strong> {appointment_date}</p>
                        <p><strong>Time:</strong> {start_time}</p>
                    </div>
                    
                    <p>Please make sure to arrive on time. If you have any questions or need to reschedule, please contact us.</p>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 Hospital Management System. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """


def appointment_cancellation_template(patient_name, doctor_name, appointment_date, start_time='', reason=''):
    """Generate HTML for appointment cancellation email"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f44336; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; border-radius: 5px; }}
                .details {{ line-height: 1.8; }}
                .footer {{ margin-top: 20px; text-align: center; color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Appointment Cancelled</h1>
                </div>
                
                <div class="content">
                    <p>Dear <strong>{patient_name}</strong>,</p>
                    
                    <p>Your appointment has been cancelled. Here are the details:</p>
                    
                    <div class="details">
                        <p><strong>Doctor:</strong> {doctor_name}</p>
                        <p><strong>Original Date:</strong> {appointment_date}</p>
                        {f'<p><strong>Time:</strong> {start_time}</p>' if start_time else ''}
                        <p><strong>Reason:</strong> {reason}</p>
                    </div>
                    
                    <p>Please visit your dashboard to reschedule or contact our support team for assistance.</p>
                </div>
                
                <div class="footer">
                    <p>&copy; 2024 Hospital Management System. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
