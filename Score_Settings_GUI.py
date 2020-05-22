import tkinter as tk
import projection_calculation as pc


# FIXME: Currently getting ValueError. Need program to wait for input in entry boxes before executing.
class ScoreGUI:

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Score Settings Calculator")
        self.win.geometry('700x400')
        # self.canvas = tk.Canvas(self.win, width=660, height=660)
        # self.canvas.pack()
        self.passing = self.pass_settings()
        self.rush = self.rush_settings()
        self.rec = self.rec_settings()
        self.kick = self.kick_settings()
        self.dst = self.dst_settings()
        # self.calculate(passing, rush, rec, kick, dst)
        self.calc_btn = tk.Button(self.win, text='Calculate', command=self.calculate)
        self.calc_btn.place(x=300, y=300)

    def calculate(self):
        player_list = pc.player_load()
        clean_player_list = pc.clean_data(player_list)
        projection_list = pc.projection_calc(clean_player_list, self.passing, self.rush, self.rec, self.kick, self.dst)
        writer = pd.ExcelWriter('projection_sheets.xlsx', engine='xlsxwriter')
        for inx, df in enumerate(projection_list):
            df.to_excel(writer, sheet_name='sheet' + str(inx))

    def pass_settings(self):
        passing_label = tk.Label(self.win, text='Passing', font=('calibre', 12, 'bold', 'underline'))

        pass_td = tk.StringVar()
        pass_td_label = tk.Label(self.win, text='Points per Pass TD',
                                 font=('calibre', 10, 'bold'))
        pass_td_entry = tk.Entry(self.win, textvariable=pass_td,
                                 font=('calibre', 10, 'normal'))
        pass_yds = tk.StringVar()
        pass_yds_label = tk.Label(self.win, text='Points per 10 Pass Yards',
                                  font=('calibre', 10, 'bold'))
        pass_yds_entry = tk.Entry(self.win, textvariable=pass_yds,
                                  font=('calibre', 10, 'normal'))
        completions = tk.StringVar()
        completions_label = tk.Label(self.win, text='Points per 10 Completions',
                                     font=('calibre', 10, 'bold'))
        completions_entry = tk.Entry(self.win, textvariable=completions,
                                     font=('calibre', 10, 'normal'))

        passing_label.grid(row=0, column=0)
        pass_td_label.grid(row=1, column=0)
        pass_td_entry.grid(row=1, column=1)
        pass_yds_label.grid(row=2, column=0)
        pass_yds_entry.grid(row=2, column=1)
        completions_label.grid(row=3, column=0)
        completions_entry.grid(row=3, column=1)

        tds = (pass_td_entry.get())
        yds = pass_yds_entry.get()
        comp = completions_entry.get()

        return {'pass_tds': tds, 'pass_yds': yds, 'completions': comp}

    def rush_settings(self):
        rushing_label = tk.Label(self.win, text='Rushing', font=('calibre', 12, 'bold', 'underline'))

        rush_td = tk.StringVar()
        rush_td_label = tk.Label(self.win, text='Points per Rush TD',
                                 font=('calibre', 10, 'bold'))
        rush_td_entry = tk.Entry(self.win, textvariable=rush_td,
                                 font=('calibre', 10, 'normal'))
        rush_yds = tk.StringVar()
        rush_yds_label = tk.Label(self.win, text='Points per 10 Rush Yards',
                                  font=('calibre', 10, 'bold'))
        rush_yds_entry = tk.Entry(self.win, textvariable=rush_yds,
                                  font=('calibre', 10, 'normal'))
        fl = tk.StringVar()
        fl_label = tk.Label(self.win, text='Points per Fumble Lost',
                            font=('calibre', 10, 'bold'))
        fl_entry = tk.Entry(self.win, textvariable=fl,
                            font=('calibre', 10, 'normal'))

        rushing_label.grid(row=5, column=0)
        rush_td_label.grid(row=6, column=0)
        rush_td_entry.grid(row=6, column=1)
        rush_yds_label.grid(row=7, column=0)
        rush_yds_entry.grid(row=7, column=1)
        fl_label.grid(row=8, column=0)
        fl_entry.grid(row=8, column=1)

        tds = rush_td_entry.get()
        yds = rush_yds_entry.get()
        fl = fl_entry.get()

        return {'rush_tds': tds, 'rush_yds': yds, 'fum_lost': fl}

    def rec_settings(self):
        receiving_label = tk.Label(self.win, text='Receiving', font=('calibre', 12, 'bold', 'underline'))

        rec_td = tk.StringVar()
        rec_td_label = tk.Label(self.win, text='Points per Rec TD',
                                font=('calibre', 10, 'bold'))
        rec_td_entry = tk.Entry(self.win, textvariable=rec_td,
                                font=('calibre', 10, 'normal'))
        rec_yds = tk.StringVar()
        rec_yds_label = tk.Label(self.win, text='Points per Rec Yards',
                                 font=('calibre', 10, 'bold'))
        rec_yds_entry = tk.Entry(self.win, textvariable=rec_yds,
                                 font=('calibre', 10, 'normal'))

        receiving_label.grid(row=10, column=0)
        rec_td_label.grid(row=11, column=0)
        rec_td_entry.grid(row=11, column=1)
        rec_yds_label.grid(row=12, column=0)
        rec_yds_entry.grid(row=12, column=1)

        tds = rec_td_entry.get()
        yds = rec_yds_entry.get()

        return {'rec_tds': tds, 'rec_yds': yds}

    def kick_settings(self):
        kick_label = tk.Label(self.win, text='Kicking', font=('calibre', 12, 'bold', 'underline'))

        pat_made = tk.StringVar()
        pat_made_label = tk.Label(self.win, text='Points per Extra Point Made',
                                  font=('calibre', 10, 'bold'))
        pat_made_entry = tk.Entry(self.win, textvariable=pat_made,
                                  font=('calibre', 10, 'normal'))
        fg_missed = tk.StringVar()
        fg_missed_label = tk.Label(self.win, text="Points per FG Missed",
                                   font=('calibre', 10, 'bold'))
        fg_missed_entry = tk.Entry(self.win, textvariable=fg_missed,
                                   font=('calibre', 10, 'normal'))
        fg_made = tk.StringVar()
        fg_made_label = tk.Label(self.win, text="Points per FG Made",
                                 font=('calibre', 10, 'bold'))
        fg_made_entry = tk.Entry(self.win, textvariable=fg_made,
                                 font=('calibre', 10, 'normal'))

        kick_label.grid(row=0, column=2)
        pat_made_label.grid(row=1, column=2)
        pat_made_entry.grid(row=1, column=3)
        fg_missed_label.grid(row=2, column=2)
        fg_missed_entry.grid(row=2, column=3)
        fg_made_label.grid(row=3, column=2)
        fg_made_entry.grid(row=3, column=3)

        xpt = pat_made_entry.get()
        made = fg_made_entry.get()
        missed = fg_missed_entry.get()

        return {'pat_made': xpt, 'fg_made': made, 'fg_missed': missed}

    def dst_settings(self):
        dst_label = tk.Label(self.win, text='Defense/Special Teams', font=('calibre', 12, 'bold', 'underline'))

        sack = tk.StringVar()
        sack_label = tk.Label(self.win, text='Points per Sack',
                              font=('calibre', 10, 'bold'))
        sack_entry = tk.Entry(self.win, textvariable=sack,
                              font=('calibre', 10, 'normal'))
        inter = tk.StringVar()
        inter_label = tk.Label(self.win, text="Points per Interception",
                               font=('calibre', 10, 'bold'))
        inter_entry = tk.Entry(self.win, textvariable=inter,
                               font=('calibre', 10, 'normal'))
        fr = tk.StringVar()
        fr_label = tk.Label(self.win, text="Points per Fumble Recovered",
                            font=('calibre', 10, 'bold'))
        fr_entry = tk.Entry(self.win, textvariable=fr,
                            font=('calibre', 10, 'normal'))
        ff = tk.StringVar()
        ff_label = tk.Label(self.win, text='Points per Forced Fumble',
                            font=('calibre', 10, 'bold'))
        ff_entry = tk.Entry(self.win, textvariable=ff,
                            font=('calibre', 10, 'normal'))
        def_td = tk.StringVar()
        def_td_label = tk.Label(self.win, text="Points per Defensive TD",
                                font=('calibre', 10, 'bold'))
        def_td_entry = tk.Entry(self.win, textvariable=def_td,
                                font=('calibre', 10, 'normal'))
        safety = tk.StringVar()
        safety_label = tk.Label(self.win, text="Points per Safety",
                                font=('calibre', 10, 'bold'))
        safety_entry = tk.Entry(self.win, textvariable=safety,
                                font=('calibre', 10, 'normal'))

        dst_label.grid(row=5, column=2)
        sack_label.grid(row=6, column=2)
        sack_entry.grid(row=6, column=3)
        inter_label.grid(row=7, column=2)
        inter_entry.grid(row=7, column=3)
        fr_label.grid(row=8, column=2)
        fr_entry.grid(row=8, column=3)
        ff_label.grid(row=9, column=2)
        ff_entry.grid(row=9, column=3)
        def_td_label.grid(row=10, column=2)
        def_td_entry.grid(row=10, column=3)
        safety_label.grid(row=11, column=2)
        safety_entry.grid(row=11, column=3)

        sk = sack_entry.get()
        pick = inter_entry.get()
        f_rec = fr_entry.get()
        f_for = ff_entry.get()
        dt = def_td_entry.get()
        sfty = safety_entry.get()

        return {'sack': sk, 'int': pick, 'fr': f_rec, 'ff': f_for, 'def_td': dt, 'safety': sfty}


ScoreGUI()
tk.mainloop()
