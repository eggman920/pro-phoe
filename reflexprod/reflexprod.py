import reflex as rx
import pandas as pd
import requests
from datetime import datetime as dt
import numpy as np
from typing import List



req = requests.session()


class Customer(rx.Model, table=True):
    """The customer model."""

    customer_name: str
    email: str
    age: int
    gender: str
    floor: str
    location: str
    job: str
    salary: int



class State(rx.State):
    """The app state."""

    customer_name: str = ""
    email: str = ""
    age: int = 0
    gender: str = "Other"
    floor: str = ""
    location: str = ""
    job: str = ""
    salary: int = 0
    users: List[Customer] = []
    products: dict[str, str] = {}
    email_content_data: str = ""
    gen_response = False
    data: pd.DataFrame


    def add_customer(self):
        #Add a customer to the database.
        with (rx.session() as session):
            session.add(
                Customer(
                    customer_name=self.customer_name,
                    email=self.email,
                    age=self.age,
                    gender=self.gender,
                    floor=self.floor,
                    location=self.location,
                    job=self.job,
                    salary=self.salary,
                        )
                )
            session.commit()
            #rx.window_alert(f"User {self.customer_name} has been added.")
        return rx.redirect("/")



    def customer_page(self):
        #The customer page.
        return rx.redirect("/")

    def onboarding_page(self):
        #The onboarding page.
        return rx.redirect("/onboarding")


    def delete_customer(self, email: str):
        #Delete a customer from the database.
        with rx.session() as session:
            session.query(Customer).filter_by(email=email).delete()
            session.commit()

    def webhook(self):
        with rx.session() as session:
            t = session.query(Customer.customer_name.label("login"), Customer.email.label("link"), Customer.gender.label("reason"),
                Customer.floor, Customer.location.label("station"), Customer.job.label("type")).statement
            print(t)

            df = pd.read_sql(t, session.bind)
            print(df)

        snap = dt.now().strftime('%a %H:%M')
        slack = ''
        msg = f'Trouble Ticket Tracker (T3) table below was manually sent at {snap}'
        df = df.to_markdown(tablefmt="plain", index=False)
        req.post(slack, json={"Header": msg, "df": df})




    @rx.var
    def get_users(self) -> List[Customer]:
        with rx.session() as session:
            users = session.query(Customer).all()
            return users


    def open_text_area(self):
        self.text_area_disabled = False

    def close_text_area(self):
        self.text_area_disabled = True

    @rx.var
    def dtfr(self) -> pd.DataFrame:
        with rx.session() as session:
            t = session.query(Customer.customer_name.label("login"),Customer.email.label("link"), Customer.gender.label("reason"), Customer.floor, Customer.location.label("station"), Customer.job.label("type")).statement
            self.df = pd.read_sql(t, session.bind)
            #new_data = self.df.value_counts(["reason", "type"])
            self.df['floor_type_count'] = self.df['floor'] + self.df['type']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)
            #cols = ['floor','reason','type']
            #self.df = self.df.join(self.df[cols].apply(lambda x: x.map(x.value_counts())).add_prefix('count_'))
            #self.df['reason_count'] = self.df.groupby(by=['reason','type']).size()
            return self.df

    @rx.var
    def statlogic(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Safety Tape' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Safety Tape' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Safety Tape']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Safety Tape' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_
    @rx.var
    def stathelptextlogic(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Safety Tape' not in self.df.values:
                self.txt="Good to go! \U0001F44D"
                return self.txt
            else:
                self.safetytape_count = self.df['gender'].value_counts()['Safety Tape']
                safetytape_count = np.uint32(self.safetytape_count).item()
                txt1="Or "
                self.txt=" Station(s) Not Ready"
                return (format(str(safetytape_count) + self.txt))

    @rx.var
    def statbglogic(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Safety Tape' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic2(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'IDS' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'IDS' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['IDS']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic2(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'IDS' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic2(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'IDS' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt
    @rx.var
    def statbglogic2(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'IDS' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg


    @rx.var
    def statlogic3(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Computer Screen' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Computer Screen' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Computer Screen']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic3(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Computer Screen' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic3(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Computer Screen' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic3(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Computer Screen' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic4(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'FC Games' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'FC Games' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['FC Games']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic4(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'FC Games' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic4(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'FC Games' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic4(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'FC Games' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg


    @rx.var
    def statlogic5(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Scanner' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Scanner' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Scanner']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic5(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Scanner' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic5(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Scanner' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic5(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Scanner' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg


    @rx.var
    def statlogic6(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Bin Filter' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Bin Filter' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Bin Filter']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic6(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Bin Filter' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic6(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Bin Filter' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic6(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Bin Filter' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg
    @rx.var
    def statlogic7(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Fan' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Fan' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Fan']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic7(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Fan' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic7(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Fan' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogi7(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Fan' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic8(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Mat' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Mat' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Mat']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic8(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Mat' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic8(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Mat' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic8(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Mat' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic9(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Rack Light' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Rack Light' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Rack Light']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic9(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Rack Light' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic9(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Rack Light' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic9(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Rack Light' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic10(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Arsaw Gate' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Arsaw Gate' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Arsaw Gate']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic10(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Arsaw Gate' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic10(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Arsaw Gate' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt

    @rx.var
    def statbglogic10(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Arsaw Gate' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic11(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Broom' not in self.df.values:
                self.ids_count = '\U0001F44D'
                return self.ids_count

            elif 'Broom' in self.df.values:
                self.ids_count = self.df['gender'].value_counts()['Broom']

                return np.uint32(self.ids_count).item()
    @rx.var
    def arrowstatlogic11(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Broom' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic11(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Broom' not in self.df.values:
                self.txt="Good to go!"
                return self.txt
            else:
                self.txt="Station(s) Not Ready"
                return self.txt
    @rx.var
    def statbglogic11(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if 'Broom' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogic12(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            return (format((1-len(self.df)/444),".2%"))


    @rx.var
    def arrowstatlogic12(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if format((1-len(new_data)/444),".2%") == "100.00%":
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stathelptextlogic12(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if format((1-len(new_data)/444),".2%") == "100.00%":
                self.txt="All Stations at MIA1 are Ready!"
                return self.txt
            else:
                ids_count = len(self.df)

                self.txt = " Station(s) at MIA1 Not Ready"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogic12(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['gender'].value_counts()
            self.df['count'] = self.df['gender'].map(new_data)

            if format((1-len(new_data)/444),".2%") == "100.00%":
                self.bg = "#63be7b"
                return self.bg
            elif format((1-len(new_data)/444),".2%") > "90.00%":
                self.bg = "#ffe666"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicoverallarsaw(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            #print(new_data)

            if 'Arsaw' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count

            elif 'Arsaw' in self.df.values:
                self.ids_count = self.df['job'].value_counts()['Arsaw']

                self.ids_count = np.uint32(self.ids_count).item()

                return (format((1-self.ids_count/128),".2%"))

    @rx.var
    def statarrowlogicoverallarsaw(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            #print(new_data)
            if 'Arsaw' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_

    @rx.var
    def stattextlogicoverallarsaw(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            #print(new_data)

            if 'Arsaw' not in self.df.values:
                self.txt="All Arsaw Stations are Ready!"
                return self.txt

            elif 'Arsaw' in self.df.values:
                ids_count = self.df['job'].value_counts()['Arsaw']

                print(ids_count)
                self.txt = " Arsaw Station(s) Not Ready"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicoverallarsaw(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            #print(new_data)

            if 'Arsaw' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg


    @rx.var
    def statlogicoveralluniversal(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            #print(new_data)

            if 'Universal' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count

            elif 'Universal' in self.df.values:
                self.ids_count = self.df['job'].value_counts()['Universal']

                self.ids_count = np.uint32(self.ids_count).item()

                return (format((1-self.ids_count/316),".2%"))

    @rx.var
    def statarrowlogicoveralluniversal(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            # print(new_data)
            if 'Universal' not in self.df.values:
                self.type_ = "increase"
                return self.type_
            else:
                self.type_ = "decrease"
                return self.type_

    @rx.var
    def stattextlogicoveralluniversal(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            # print(new_data)

            if 'Universal' not in self.df.values:
                self.txt = "All Universal Stations are Ready!"
                return self.txt
            else:
                self.ids_count = self.df['job'].value_counts()['Universal']

                self.ids_count = np.uint32(self.ids_count).item()
                self.txt = " Universal Station(s) Not Ready"
                return (format(str(self.ids_count) + self.txt))

    @rx.var
    def statbglogicoveralluniversal(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            new_data = self.df['job'].value_counts()
            self.df['count'] = self.df['job'].map(new_data)
            # print(new_data)

            if 'Universal' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA01(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Arsaw' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:
                self.ids_count = (self.df['floor_type_count'].value_counts()['A01Arsaw'])
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1-self.ids_count/32),".2%"))

    @rx.var
    def arrowstatlogicA01(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Arsaw' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_
    @rx.var
    def stathelptextlogicA01(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Arsaw' not in self.df.values:
                self.txt="All Arsaw Stations on A01 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A01Arsaw']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Arsaw Station(s) Not Ready on A01"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA01(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Arsaw' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA02(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Arsaw' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:

                self.ids_count = self.df['floor_type_count'].value_counts()['A02Arsaw']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1-self.ids_count/32),".2%"))

    @rx.var
    def arrowstatlogicA02(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Arsaw' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_
    @rx.var
    def stathelptextlogicA02(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Arsaw' not in self.df.values:
                self.txt="All Arsaw Stations on A02 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A02Arsaw']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Station(s) Not Ready"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA02(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Arsaw' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA03(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Arsaw' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:

                self.ids_count = self.df['floor_type_count'].value_counts()['A03Arsaw']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1-self.ids_count/32),".2%"))

    @rx.var
    def arrowstatlogicA03(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Arsaw' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_
    @rx.var
    def stathelptextlogicA03(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Arsaw' not in self.df.values:
                self.txt="All Arsaw Stations on A03 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A03Arsaw']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Station(s) Not Ready"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA03(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Arsaw' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA04(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Arsaw' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:
                self.ids_count = self.df['floor_type_count'].value_counts()['A04Arsaw']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1-self.ids_count/32),".2%"))

    @rx.var
    def arrowstatlogicA04(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Arsaw' not in self.df.values:
                self.type_="increase"
                return self.type_
            else:
                self.type_="decrease"
                return self.type_
    @rx.var
    def stathelptextlogicA04(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Arsaw' not in self.df.values:
                self.txt="All Arsaw Stations on A04 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A04Arsaw']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Station(s) Not Ready"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA04(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Arsaw' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA01uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Universal' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:
                self.ids_count = (self.df['floor_type_count'].value_counts()['A01Universal'])
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1 - self.ids_count / 79), ".2%"))

    @rx.var
    def arrowstatlogicA01uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Universal' not in self.df.values:
                self.type_ = "increase"
                return self.type_
            else:
                self.type_ = "decrease"
                return self.type_

    @rx.var
    def stathelptextlogicA01uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Universal' not in self.df.values:
                self.txt = "All Universal Stations on A01 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A01Universal']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Universal(s) Not Ready on A01"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA01uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A01Universal' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA02uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Universal' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:

                self.ids_count = self.df['floor_type_count'].value_counts()['A02Universal']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1 - self.ids_count / 76), ".2%"))

    @rx.var
    def arrowstatlogicA02uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Universal' not in self.df.values:
                self.type_ = "increase"
                return self.type_
            else:
                self.type_ = "decrease"
                return self.type_

    @rx.var
    def stathelptextlogicA02uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Universal' not in self.df.values:
                self.txt = "All Universal Stations on A02 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A02Universal']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Universal(s) Not Ready on A02"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA02uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A02Universal' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA03uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Universal' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:

                self.ids_count = self.df['floor_type_count'].value_counts()['A03Universal']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1 - self.ids_count / 79), ".2%"))

    @rx.var
    def arrowstatlogicA03uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Universal' not in self.df.values:
                self.type_ = "increase"
                return self.type_
            else:
                self.type_ = "decrease"
                return self.type_

    @rx.var
    def stathelptextlogicA03uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Universal' not in self.df.values:
                self.txt = "All Universal Stations on A03 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A03Universal']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Universal(s) Not Ready on A03"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA03uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A03Universal' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg

    @rx.var
    def statlogicA04uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Universal' not in self.df.values:
                self.ids_count = '100%'
                return self.ids_count
            else:
                self.ids_count = self.df['floor_type_count'].value_counts()['A04Universal']
                self.ids_count = np.uint32(self.ids_count).item()
                return (format((1 - self.ids_count / 82), ".2%"))

    @rx.var
    def arrowstatlogicA04uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Universal' not in self.df.values:
                self.type_ = "increase"
                return self.type_
            else:
                self.type_ = "decrease"
                return self.type_

    @rx.var
    def stathelptextlogicA04uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Universal' not in self.df.values:
                self.txt = "All Universal Stations on A04 Ready!"
                return self.txt
            else:
                ids_count = self.df['floor_type_count'].value_counts()['A04Universal']

                ids_count = np.uint32(ids_count).item()
                self.txt = " Universal(s) Not Ready on A04"
                return (format(str(ids_count) + self.txt))

    @rx.var
    def statbglogicA04uni(self):
        with rx.session() as session:
            t = session.query(Customer).statement
            self.df = pd.read_sql(t, session.bind)
            self.df['floor_type_count'] = self.df['floor'] + self.df['job']
            new_data = self.df['floor_type_count'].value_counts()
            self.df['count'] = self.df['floor_type_count'].map(new_data)

            if 'A04Universal' not in self.df.values:
                self.bg = "#63be7b"
                return self.bg
            else:
                self.bg = "#f8696b"
                return self.bg




def navbar():
    #The navbar for the top of the page.
    return (
     rx.box(
        rx.hstack(
            rx.tooltip(
                rx.hstack(
                    rx.image(src="MIA1 concept.png", width="50px"),
                        rx.text(
                        "Project Phoenix",
                        background_image="linear-gradient(271.68deg, #F8961E 0.75%, #F9C74F 88.52%)",
                        background_clip="text",
                        font_family="Helvetica",
                        font_weight="bold",
                        font_size="2em",
                    ),
                ),
                label="The values in the Dashboard are dependent on the data entered \n"
                      "into Table BELOW, named Trouble Ticket Tracker.\n"
                      "Submitting a ticket alone will not update the Dashboard. \n"
                      "You must copy link and paste into link field when creating \n"
                      "a new entry below",
                should_wrap_children=True),
            rx.color_mode_button(rx.color_mode_icon()),
            rx.spacer(),
            rx.menu(
                rx.menu_button(
                    "Menu", bg="black", color="white", border_radius="md", px=4, py=2
                ),
                rx.menu_list(
                    rx.link(
                        rx.menu_item(
                            rx.hstack(
                                rx.text("Home"), rx.icon(tag="hamburger")
                            )
                        ),
                        href="/",
                    ),
                    rx.menu_divider(),
                    rx.link(
                        rx.menu_item(
                            rx.hstack(rx.text("Audit"), rx.icon(tag="add"))
                        ),
                        href="/onboarding",
                    ),
                ),
            ),
            justify="space-between",
            border_bottom="0.2em",
            padding_x="2em",
            padding_y="1em",

        ),
        position="flex",
        width="100%",
        top="0px",
        z_index="500",
    ))

def show_customer(user:Customer):
    #Show a customer in a table row.
    return (
        rx.tr(
        rx.td(user.customer_name),
                rx.td(
                    rx.link(
                        rx.button(
                            "link to ticket",
                            border_radius=".3em",
                            box_shadow="linear-gradient(271.68deg, #4D908E 0.75%, #43AA8B 88.52%)",
                            background_image="linear-gradient(271.68deg, #4D908E 0.75%, #43AA8B 88.52%)",
                            box_sizing="border-box",
                            color="black",
                            opacity="0.8",
                            _hover={
                                "opacity": 1,
                            },
                        ),
                        href=user.email,
                        is_external=True,
                    ),
                ),
        rx.td(user.gender),
        rx.td(user.floor),
        rx.td(user.location),
        rx.td(user.job),

        rx.td(rx.tooltip(
            rx.button(
                "Delete",
                on_click=lambda: State.delete_customer(user.email),
                bg="linear-gradient(#F9844A 0.75%, #E1306C 88.52%)",
                color="black",
                opacity="0.8",
                _hover={
                    "opacity": 1,
                },
            ),label=" \U000026A0 Before deleting row, please click the \"link to ticket\" button and verify that the original ticket has been resolved \U000026A0",
                                       should_wrap_children=True
                                       ),
        ),
        )
    )



def testingsomething():
    #The navbar for the top of the page.
    return (
     rx.box(
         rx.hstack(
         rx.box(
                 rx.stat(
                     rx.stat_label("Overall Readiness"),
                     rx.stat_number(State.statlogic12),
                     rx.stat_help_text(f"{State.stathelptextlogic12}", rx.stat_arrow(type_=f"{State.arrowstatlogic12}"))
                 ),
                 align="center",
                 bg=State.statbglogic12,
                 border_radius="md",
                 width="100%"
             ),
             justify="space-between",
             border_bottom="0.5em",
             padding_x="25em",
             padding_y="1em",
         ),
         rx.hstack(

             rx.box(
                 rx.stat(
                     rx.stat_label("Overall Arsaw Readiness"),
                     rx.stat_number(State.statlogicoverallarsaw),

                     rx.stat_help_text(f"{State.stattextlogicoverallarsaw}", rx.stat_arrow(type_=f"{State.statarrowlogicoverallarsaw}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicoverallarsaw,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("Overall Universal Readiness"),
                     rx.stat_number(State.statlogicoveralluniversal),

                     rx.stat_help_text(f"{State.stattextlogicoveralluniversal}", rx.stat_arrow(type_=f"{State.statarrowlogicoveralluniversal}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicoveralluniversal,
                 border_radius="md",
                 width="100%",
             ),
             justify="space-between",
             border_bottom="0.2em",
             padding_x="15em",
             padding_y="1em",
         ),
         rx.hstack(
             rx.box(
                 rx.stat(
                     rx.stat_label("A01 Arsaw Readiness"),
                     rx.stat_number(State.statlogicA01),

                     rx.stat_help_text(f"{State.stathelptextlogicA01}")
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA01,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A02 Arsaw Readiness"),
                     rx.stat_number(State.statlogicA02),

                     rx.stat_help_text(f"{State.stathelptextlogicA02}")
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA02,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A03 Arsaw Readiness"),
                     rx.stat_number(State.statlogicA03),

                     rx.stat_help_text(f"{State.stathelptextlogicA03}")
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA03,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A04 Arsaw Readiness"),
                     rx.stat_number(State.statlogicA04),

                     rx.stat_help_text(f"{State.stathelptextlogicA04}")
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA04,
                 border_radius="md",
                 width="100%",
             ),

             justify="space-between",
             border_bottom="0.1em",
             padding_x="2em",
             padding_y="1em",
         ),
         rx.hstack(
             rx.box(
                 rx.stat(
                     rx.stat_label("A01 Universal Readiness"),
                     rx.stat_number(State.statlogicA01uni),

                     rx.stat_help_text(f"{State.stathelptextlogicA01uni}", rx.stat_arrow(type_=f"{State.arrowstatlogicA01uni}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA01uni,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A02 Universal Readiness"),
                     rx.stat_number(State.statlogicA02uni),

                     rx.stat_help_text(f"{State.stathelptextlogicA02uni}", rx.stat_arrow(type_=f"{State.arrowstatlogicA02uni}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA02uni,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A03 Universal Readiness"),
                     rx.stat_number(State.statlogicA03uni),

                     rx.stat_help_text(f"{State.stathelptextlogicA03uni}", rx.stat_arrow(type_=f"{State.arrowstatlogicA03uni}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA03uni,
                 border_radius="md",
                 width="100%",
             ),
             rx.box(
                 rx.stat(
                     rx.stat_label("A04 Universal Readiness"),
                     rx.stat_number(State.statlogicA04uni),

                     rx.stat_help_text(f"{State.stathelptextlogicA04uni}", rx.stat_arrow(type_=f"{State.arrowstatlogicA04uni}"))
                     ,
                 ),
                 align="center",
                 bg=State.statbglogicA04uni,
                 border_radius="md",
                 width="100%",
             ),

             justify="space-between",
             border_bottom=".1em",
             padding_x="2em",
             padding_y="1em",
         ),
        rx.hstack(
            rx.box(
                rx.stat(
                    rx.stat_label("Safety Tape"),
                    rx.stat_number(State.statlogic),

                    rx.stat_help_text(f"{State.stathelptextlogic}")
                    ,
                ),
                align="center",
                bg=State.statbglogic,
                border_radius="md",
                width="100%",
            )
            ,
            rx.box(
                rx.stat(
                    rx.stat_label("IDS"),
                    rx.stat_number(State.statlogic2),
                    rx.stat_help_text(f"{State.stathelptextlogic2}", rx.stat_arrow(type_=f"{State.arrowstatlogic2}"))
                ),
                align="center",
                bg=State.statbglogic2,
                border_radius="md",
                width="100%"
            )
,            rx.box(
                rx.stat(
                    rx.stat_label("Computer Screen"),
                    rx.stat_number(State.statlogic3),
                    rx.stat_help_text(f"{State.stathelptextlogic3}", rx.stat_arrow(type_=f"{State.arrowstatlogic3}"))
                ),
                align="center",
                bg=State.statbglogic3,
                border_radius="md",
                width="100%"
            )
            ,
            rx.box(
                rx.stat(
                    rx.stat_label("FC Games"),
                    rx.stat_number(State.statlogic4),
                    rx.stat_help_text(f"{State.stathelptextlogic4}", rx.stat_arrow(type_=f"{State.arrowstatlogic4}"))
                ),
                align="center",
                bg=State.statbglogic4,
                border_radius="md",
                width="100%"
            ),

            rx.box(
                rx.stat(
                    rx.stat_label("Scanner"),
                    rx.stat_number(State.statlogic5),
                    rx.stat_help_text(f"{State.stathelptextlogic5}", rx.stat_arrow(type_=f"{State.arrowstatlogic5}"))
                ),
                align="center",
                bg=State.statbglogic5,
                border_radius="md",
                width="100%"
            ),

            rx.box(
                rx.stat(
                    rx.stat_label("Bin Filter"),
                    rx.stat_number(State.statlogic6),
                    rx.stat_help_text(f"{State.stathelptextlogic6}", rx.stat_arrow(type_=f"{State.arrowstatlogic6}"))
                ),
                align="center",
                bg=State.statbglogic6,
                border_radius="md",
                width="100%"
            ),
            justify="space-between",
            border_bottom="0.1em",
            padding_x="2em",
            padding_y="1em",

        ),
        rx.hstack(
         rx.box(
             rx.stat(
                 rx.stat_label("Fan"),
                 rx.stat_number(State.statlogic7),
                 rx.stat_help_text(f"{State.stathelptextlogic7}", rx.stat_arrow(type_=f"{State.arrowstatlogic7}"))
             ),
             align="center",
             bg=State.statbglogi7,
             border_radius="md",
             width="100%"
         ),

         rx.box(
             rx.stat(
                 rx.stat_label("Mat"),
                 rx.stat_number(State.statlogic8),
                 rx.stat_help_text(f"{State.stathelptextlogic8}", rx.stat_arrow(type_=f"{State.arrowstatlogic8}"))
             ),
             align="center",
             bg=State.statbglogic8,
             border_radius="md",
             width="100%"
         ),

         rx.box(
             rx.stat(
                 rx.stat_label("Rack Light"),
                 rx.stat_number(State.statlogic9),
                 rx.stat_help_text(f"{State.stathelptextlogic9}", rx.stat_arrow(type_=f"{State.arrowstatlogic9}"))
             ),
             align="center",
             bg=State.statbglogic9,
             border_radius="md",
             width="100%"
         ),

         rx.box(
             rx.stat(
                 rx.stat_label("Arsaw Gate"),
                 rx.stat_number(State.statlogic10),
                 rx.stat_help_text(f"{State.stathelptextlogic10}", rx.stat_arrow(type_=f"{State.arrowstatlogic10}"))
             ),
             align="center",
             bg=State.statbglogic10,
             border_radius="md",
             width="100%"
         ),

         rx.box(
             rx.stat(
                 rx.stat_label("Broom"),
                 rx.stat_number(State.statlogic11),
                 rx.stat_help_text(f"{State.stathelptextlogic11}", rx.stat_arrow(type_=f"{State.arrowstatlogic11}"))
             ),
             align="center",
             bg=State.statbglogic11,
             border_radius="md",
             width="100%"
         ),
            justify="space-between",
            border_bottom="0.2em",
            padding_x="2em",
            padding_y=".2em"
        ),

        position="flex",
        width="70%",
        #top="0px",
        #z_index="500",

    ))


def add_customer():
    #Add a customer to the database.
    return (rx.center(
        rx.vstack(
            rx.heading("Audit Details"),
            rx.input(placeholder="Auditor Login", on_blur=State.set_customer_name),
            rx.input(placeholder="link to ticket", on_blur=State.set_email),
            rx.select(
                ["A01","A02","A03","A04"],
                placeholder="Select Floor",
                on_change=State.set_floor,
            ),
            rx.select(
                ["Arsaw", "Universal"],
                placeholder="Station Type",
                on_change=State.set_job,
            ),

            rx.input(placeholder="Station #", on_blur=State.set_location),
            rx.select(
                ["Computer Screen", "FC Games", "Scanner","IDS","Bin Filter","Fan","Mat","Safety Tape", "Rack Light", "Arsaw Gate", "Broom"],
                placeholder="Select Reason",
                on_change=State.set_gender,
            ),
            rx.button_group(rx.tooltip(rx.button("Submit", on_click=State.add_customer),
                                       label=" \U0001F4A1 Please verify you've entered all data correctly before submitting \U0001F4A1",
                                       should_wrap_children=True
                                       ),
                rx.button(rx.icon(tag="arrow_back"), on_click=State.customer_page),
                is_attached=False,
                spacing=30,
            ),
            box_shadow="lg",
            bg="",
            padding="1em",
            border="1px solid #ddd",
            border_radius="25px",
        ),
        padding_top="10em",
    ))


def delete_solved_ticket():
    #Add a customer to the database.
    return (rx.center(
        rx.vstack(
            rx.heading("Remove Entry"),
            rx.input(placeholder="Enter link to ticket", on_blur=State.set_email),

            rx.button_group(rx.button("Delete", on_click=State.delete_customer),
                rx.button(rx.icon(tag="arrow_back"), on_click=State.customer_page),
                is_attached=False,
                spacing=30,
            ),
            box_shadow="lg",
            bg="",
            padding="1em",
            border="1px solid #ddd",
            border_radius="25px",
        ),
        padding_top="10em",
    ))

def dftest():
    with rx.session() as session:
        t = session.query(Customer.customer_name.label("login"), Customer.email.label("link"), Customer.gender.label("reason"), Customer.floor,
                          Customer.location.label("station"), Customer.job.label("type")).statement
        df = pd.read_sql(t, session.bind)
        # new_data = self.df.value_counts(["reason", "type"])
        rows = df.values.tolist()
        print(rows)
        return rows

#def get_users():
#    with rx.session() as session:
#        users = session.query(Customer).all()
#        users = pd.read_sql(users, session.bind)
#        rows = users.values.tolist()
#        return rows


def index():

    #The main page.
    return (
        rx.vstack(navbar(),
        testingsomething(),
                  rx.vstack(
                  rx.markdown("""**Step 1**: Click the **Create Ticket** button, This will open a new window for you so sumbit a ticket"""),
                  rx.markdown("""**Step 2**: **Copy the link** of the ticket you just created which should look something like this - https://t.corp.amazon.com/Vxxxxxx"""),
                  rx.markdown("""**Step 3**: Click the **Create New Entry** button, you will be directed to a new page. Here you will fill out the corresponding information and paste the link you just copied into the Ticket field. Once all fields are filled click submit"""),

                      padding_top="1em",
                      width="70%",
                      align_items="center",
                  ),
            rx.vstack(
                rx.tablet_and_desktop(


                rx.hstack(
                    rx.heading(
                        rx.text(
                            "Trouble Ticket Tracker",
                            background_image="linear-gradient(271.68deg, #F8961E 0.75%, #F9C74F 88.52%)",
                            background_clip="text",
                            font_family= "Helvetica",
                            #font_weight="bold",
                            font_size=".9em",
                        )),
                    rx.link(
                        rx.button(
                            "Create Ticket",
                            border_radius=".3em",
                            bg="linear-gradient(271.68deg, #F8961E 0.75%, #F9C74F 99.52%)",
                            box_sizing="border-box",
                            color="black",
                            opacity="0.8",
                            _hover={
                                "opacity": 1,
                            },
                        ),
                        href="https://archer-na.corp.amazon.com/?warehouseID=MIA1",
                        is_external=True,
                    ),
                    rx.button(
                        "Create New Entry",
                        on_click=State.onboarding_page,
                        bg="linear-gradient(271.68deg, #277DA1 0.75%, #43AA8B 88.52%)",
                        color="black",
                        opacity="0.8",
                        _hover={
                            "opacity": 1,
                        },),
                    rx.button(
                        "Send Slack ",
                        rx.icon(tag="email"),
                        on_click=State.webhook(),
                        bg="linear-gradient(271.68deg, #833AB4 0.75%, #F56040 88.52%)",
                        color="black",
                        opacity="0.8",
                        _hover={
                            "opacity": 1,
                        },
                    )
                ),
                rx.table_container(
                   rx.table(
                        rx.thead(
                            rx.tr(
                                rx.th("Auditor Login"),
                                rx.th("link to ticket"),
                                rx.th("Reason"),
                                rx.th("Floor"),
                                rx.th("Station #"),
                                rx.th("Station Type"),
                                rx.th("Delete"),
                            )
                        ),
                        rx.tbody(rx.foreach(State.get_users, show_customer)),
                   ),
                    bg=" ",
                    border="1px solid #ddd",
                    border_radius="5px",
                ),
                align_items="right",
                padding_top="1em",
            ),

               rx.data_table(
                   data=State.dtfr,
                   pagination=True,
                   search=True,
                   sort=True,
                   resizable=True,
               ),
                rx.divider(),
                padding_top="1em",
                width="70%",
                align_items="center",
            ),
                  width="100%",
                  align_items="center"
                  ))


FONT = "Helvectica"

style= {
    rx.Text:{
    "font_size": ["100%","115%","130%","135%","125%"],
    "font_family": FONT,
    "transition": "all 650ms ease",
    "text_align": "center"},
    rx.Heading:{
    "font_size": ["250%", "275%", "300%", "325%", "350%"],
    "text_align": "center",
    "transition": "all 650ms ease"
},}
# Add state and page to the app.
app = rx.App(state=State, style=style)
app.add_page(index, title="Project Phoenix - Home")
app.add_page(add_customer, "/onboarding", title="Project Phoenix - Audit")

app.compile()




