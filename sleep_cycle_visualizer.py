import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class SleepTracker:

    def __init__(self, file_name="sleep_data.csv"):
        self.file_name = file_name

        if not os.path.exists(self.file_name):
            df = pd.DataFrame(columns=["Date","Day","Week","Hours"])
            df.to_csv(self.file_name, index=False)

    def add_entry(self, date, hours):
        try:
            df = pd.read_csv(self.file_name)

            # Validate date
            date_obj = pd.to_datetime(date)

            # Validate hours
            if hours < 0 or hours > 24:
                return df, "Invalid hours! Enter between 0–24."

            day = date_obj.day_name()
            week = date_obj.isocalendar().week

            new_data = pd.DataFrame([[date, day, week, hours]],
                                    columns=["Date","Day","Week","Hours"])

            df = pd.concat([df,new_data], ignore_index=True)
            df.to_csv(self.file_name, index=False)

            return df, "Entry added successfully!"

        except Exception as e:
            return pd.DataFrame(), f"Error: {str(e)}"


    def get_data(self):
        try:
            return pd.read_csv(self.file_name)
        except:
            return pd.DataFrame()


    def clear_data(self):
        try:
            df = pd.DataFrame(columns=["Date","Day","Week","Hours"])
            df.to_csv(self.file_name, index=False)
            return df, "All data cleared!"
        except Exception as e:
            return pd.DataFrame(), f"Error: {str(e)}"


    def generate_visualizations(self):
        try:
            df = pd.read_csv(self.file_name)

            if df.empty:
                return None,None,None,None,None

            sns.set_style("whitegrid")

            # Line plot
            plt.figure()
            sns.lineplot(data=df, x="Date", y="Hours", marker="o")
            plt.xticks(rotation=45)
            line_chart = plt.gcf()
            plt.close()

            # Histogram
            plt.figure()
            sns.histplot(df["Hours"], bins=6, kde=True)
            hist_chart = plt.gcf()
            plt.close()

            # Box plot
            plt.figure()
            sns.boxplot(y=df["Hours"])
            box_chart = plt.gcf()
            plt.close()

            # Weekly average
            weekly_avg = df.groupby("Week")["Hours"].mean().reset_index()
            plt.figure()
            sns.barplot(data=weekly_avg, x="Week", y="Hours")
            weekly_chart = plt.gcf()
            plt.close()

            # Heatmap
            pivot = df.pivot_table(values="Hours",
                                   index="Day",
                                   columns="Week",
                                   aggfunc="mean")

            plt.figure()
            sns.heatmap(pivot, annot=True, cmap="coolwarm")
            heatmap_chart = plt.gcf()
            plt.close()

            return line_chart, hist_chart, box_chart, weekly_chart, heatmap_chart

        except Exception as e:
            print("Visualization Error:", e)
            return None,None,None,None,None


tracker = SleepTracker()


def add_sleep(date, hours):
    return tracker.add_entry(date, hours)

def clear_sleep():
    return tracker.clear_data()

def visualize():
    return tracker.generate_visualizations()


with gr.Blocks(title="Sleep Cycle Analyzer") as app:

    gr.Markdown("# 💤 Sleep Cycle Analyzer")
    gr.Markdown("Track your sleep patterns and generate weekly reports.")

    with gr.Row():
        date_input = gr.Textbox(label="Enter Date (YYYY-MM-DD)")
        hours_input = gr.Slider(0,12,step=0.5,label="Sleep Hours")

    with gr.Row():
        add_btn = gr.Button("Add Entry")
        vis_btn = gr.Button("Generate Visualizations")
        clear_btn = gr.Button("Clear Data")

    status = gr.Textbox(label="Status")
    data_table = gr.Dataframe(label="Sleep Data")

    with gr.Row():
        line_plot = gr.Plot(label="Sleep Trend")
        hist_plot = gr.Plot(label="Sleep Distribution")

    with gr.Row():
        box_plot = gr.Plot(label="Sleep Variation")
        weekly_plot = gr.Plot(label="Weekly Average")

    heatmap_plot = gr.Plot(label="Sleep Heatmap")

    add_btn.click(add_sleep, inputs=[date_input, hours_input], outputs=[data_table, status])
    clear_btn.click(clear_sleep, outputs=[data_table, status])
    vis_btn.click(visualize, outputs=[line_plot, hist_plot, box_plot, weekly_plot, heatmap_plot])

app.launch()