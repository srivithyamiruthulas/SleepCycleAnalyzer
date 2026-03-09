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

        df = pd.read_csv(self.file_name)

        date_obj = pd.to_datetime(date)

        day = date_obj.day_name()
        week = date_obj.isocalendar().week

        new_data = pd.DataFrame([[date, day, week, hours]],
                                columns=["Date","Day","Week","Hours"])

        df = pd.concat([df,new_data], ignore_index=True)

        df.to_csv(self.file_name, index=False)

        return df, "Entry added successfully!"

    def get_data(self):
        return pd.read_csv(self.file_name)

    def clear_data(self):

        df = pd.DataFrame(columns=["Date","Day","Week","Hours"])
        df.to_csv(self.file_name, index=False)

        return df, "All data cleared!"

    def generate_visualizations(self):

        df = pd.read_csv(self.file_name)

        if df.empty:
            return None,None,None,None,None

        sns.set_style("whitegrid")

        
        plt.figure()
        sns.lineplot(data=df, x="Date", y="Hours", marker="o")
        plt.xticks(rotation=45)
        plt.title("Sleep Trend Over Time")
        line_chart = plt.gcf()
        plt.close()

    
        
        plt.figure()
        sns.histplot(df["Hours"], bins=6, kde=True)
        plt.title("Sleep Hours Distribution")
        hist_chart = plt.gcf()
        plt.close()

        
        
        plt.figure()
        sns.boxplot(y=df["Hours"])
        plt.title("Sleep Variation")
        box_chart = plt.gcf()
        plt.close()

        
        
        weekly_avg = df.groupby("Week")["Hours"].mean().reset_index()

        plt.figure()
        sns.barplot(data=weekly_avg, x="Week", y="Hours")
        plt.title("Weekly Average Sleep")
        weekly_chart = plt.gcf()
        plt.close()


        pivot = df.pivot_table(values="Hours",
                               index="Day",
                               columns="Week",
                               aggfunc="mean")

        plt.figure()
        sns.heatmap(pivot, annot=True, cmap="coolwarm")
        plt.title("Sleep Pattern Heatmap")
        heatmap_chart = plt.gcf()
        plt.close()

        return line_chart, hist_chart, box_chart, weekly_chart, heatmap_chart


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

   
    gr.Markdown("## Add Sleep Entry")

    with gr.Row():
        date_input = gr.Textbox(label="Enter Date (YYYY-MM-DD)")
        hours_input = gr.Slider(0,12,step=0.5,label="Sleep Hours")

    with gr.Row():
        add_btn = gr.Button("Add Entry")
        vis_btn = gr.Button("Generate Visualizations")
        clear_btn = gr.Button("Clear Data")

    status = gr.Textbox(label="Status")

    
    gr.Markdown("## Stored Sleep Records")
    data_table = gr.Dataframe(label="Sleep Data")

    
    gr.Markdown("## Sleep Analysis")

    with gr.Row():
        line_plot = gr.Plot(label="Sleep Trend")
        hist_plot = gr.Plot(label="Sleep Distribution")

    with gr.Row():
        box_plot = gr.Plot(label="Sleep Variation")
        weekly_plot = gr.Plot(label="Weekly Average")

    heatmap_plot = gr.Plot(label="Sleep Heatmap")

    
    add_btn.click(
        add_sleep,
        inputs=[date_input, hours_input],
        outputs=[data_table, status]
    )

    clear_btn.click(
        clear_sleep,
        outputs=[data_table, status]
    )

    vis_btn.click(
        visualize,
        outputs=[line_plot, hist_plot, box_plot, weekly_plot, heatmap_plot]
    )

app.launch()