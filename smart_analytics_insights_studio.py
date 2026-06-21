import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
import random

path = input("enter the file path: ").strip().strip('"').strip("'")
df = None
try:
    if not os.path.exists(path):
        print("FILE NOT FOUND")
    else:
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        elif path.endswith('.xlsx'):
            df = pd.read_excel(path)
        print(df)
except Exception as e:
    print(e)

if df is None:
    print("No valid file was loaded. Exiting.")
    sys.exit()

print("1ST 5 ROWS DISPLAYED SUCCESSFULLY")
print(df.head(5))
print(f"TOTAL ROWS: {len(df.index)}")
print(f"TOTAL COLOUMNS: {len(df.columns)}")
print(f"DATA TYPES OF COLOUMN: {df.dtypes}")

try:
    p = input("CONTINUE TO ANALYSIS ?? (yes/no)")
except ValueError as e:
    print({e})
    p = "no"

if p.lower() == "yes":
    print("proceeding to Dataset inspection......")
    print("_____________________________________________________________________")
    print(f"The shape of the provided Dataframe {df.shape}")
    print(f"Memory Usage {df.memory_usage()}")
    # FIX: axis=1 is row-wise, no axis is column-wise -- labels were swapped
    print(f"Number of missing values coloumn wise {df.isnull().sum()}")
    print(f"Number of missing values row wise {df.isnull().sum(axis=1)}")
    print(f"Number of dublicate values {df.duplicated().sum()}")
    print()
    print("NUMERIC COLOUMNS DISPLAYED...")
    print(df.select_dtypes(include='number'))
    print()
    print("STATISTICAL SUMMARY OF THE DATASET")
    print(df.describe())
    print()
    print("CATEGORICAL COLOUMNS DISPLAYED...")
    print(df.select_dtypes(include='object'))
    print()
    print("CORRELATION MATRIX")
    print(df.corr(numeric_only=True))
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

try:
    p = input("VIEW DATASET HEATH SCORE ?? (yes/no)")
except ValueError as e:
    print({e})
    p = "no"

if p.lower() == "yes":
    print("proceeding to Dataset inspection......")
    print("_____________________________________________________________________")
    health_score = 100
    # FIX: same axis swap as above, labels corrected
    missc = df.isnull().sum()
    missr = df.isnull().sum(axis=1)
    dup = df.duplicated().sum()
    print(f"Number of missing values coloumn wise {missc}")
    print(f"Number of missing values row wise {missr}")
    print(f"Number of dublicate values {dup}")
    if missc.sum() > 0:
        health_score -= 20
    if missr.sum() > 0:
        health_score -= 10
    if dup > 0:
        health_score -= 15
    print(f"HEALTH SCORE: {health_score}/100")
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

try:
    p = input("DO YOU WANT TO CLEAN THE DATA ?? (yes/no)")
except ValueError as e:
    print({e})
    p = "no"

if p.lower() == "yes":
    print("_____________________________________________________________________")
    print('''Choose the cleaning option:
           1. remove missing values
           2. Fill missing values
           3. interpolate missing values
           4. remove dublicate records
           5. drop empty coloumns
           6. replace values
           7. rename coloumns
           8. convert datatypes
           9. strip extra spaces
           10. standardize text values
           ''')
    try:
        choice = int(input("Enter your choice: "))
    except ValueError as e:
        print({e})
        choice = 0

    if choice == 1:
        df.dropna(inplace=True)
        print(df)
    elif choice == 2:
        df.fillna(0, inplace=True)
        print(df)
    elif choice == 3:
        print('''Choose the method:
             1. linear
             2. nearest
             3. polynomial''')
        try:
            # FIX: renamed to interp_choice instead of reusing outer "choice"
            interp_choice = int(input("Enter your choice: "))
        except ValueError as e:
            print({e})
            interp_choice = 0
        if interp_choice == 1:
            df.interpolate(method='linear', inplace=True)
            print(df)
        elif interp_choice == 2:
            df.interpolate(method='nearest', inplace=True)
            print(df)
        elif interp_choice == 3:
            # FIX: polynomial interpolation fails (TypeError) on non-numeric
            # columns when applied to the whole dataframe -- restrict to
            # numeric columns only, matching the original intent.
            numeric_cols = df.select_dtypes(include='number').columns
            df[numeric_cols] = df[numeric_cols].interpolate(method='polynomial', order=2)
            print(df)
        else:
            print("invalid choice")
    elif choice == 4:
        df.drop_duplicates(inplace=True)
        print(df)
    elif choice == 5:
        df.dropna(axis=1, inplace=True)
        print(df)
    elif choice == 6:
        r = input("enter the word to replace")
        df.replace(0, r, inplace=True)
        print(df)
    elif choice == 7:
        old_name = input("enter the old name")
        new_name = input("enter the new name")
        df.rename(columns={old_name: new_name}, inplace=True)
        print(df)
    elif choice == 8:
        coloumn_name = input("enter the coloumn name")
        data_type = input("enter the data type")
        df[coloumn_name] = df[coloumn_name].astype(data_type)
        print(df)
    elif choice == 9:
        df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
        print(df)
    elif choice == 10:
        df = df.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
        print(df)
    else:
        print("invalid choice")
else:
    print("contiuing with the existing Dataset......")
    numeric = df.select_dtypes(include="number").columns.tolist()
    catagory = df.select_dtypes(include="object").columns.tolist()
    date = df.select_dtypes(include="datetime").columns.tolist()
    print(f"NUMERIC COLOUMNS: {numeric}")
    print(f"CATEGORICAL COLOUMNS: {catagory}")
    print(f"DATE COLOUMNS: {date}")

    percent = [col for col in df.columns if '%' in col.lower() or 'percent' in col.lower()]
    print(f"PERCENT COLOUMNS: {percent}")
    revenue = [col for col in df.columns if 'revenue' in col.lower() or 'income' in col.lower()]
    print(f"REVENUE COLOUMNS: {revenue}")
    sales = [col for col in df.columns if 'sales' in col.lower()]
    print(f"SALES COLOUMNS: {sales}")
    quantity = [col for col in df.columns if 'quantity' in col.lower() or 'qty' in col.lower()]
    print(f"QUANTITY COLOUMNS: {quantity}")
    id = [col for col in df.columns if 'id' in col.lower()]
    print(f"ID COLOUMNS: {id}")
    target = [col for col in df.columns if 'target' in col.lower() or 'label' in col.lower()]
    if not target and len(df.columns) > 0:
        target = df.columns[-1]
    print(f"TARGET COLOUMNS: {target}")

    graph = None
    if date and numeric:
        graph = "line plot"
    if catagory and numeric:
        print("Recomended: Bar plot")
        graph = "Bar plot"
    if len(numeric) == 1:
        graph = "Histogram / Box plot"
    if len(numeric) == 2:
        graph = "scatter plot"
    if percent:
        graph = "Pie chart"
    if catagory and len(numeric) > 0:
        graph = "scatter / line plot"

    confirm = input("GENERATE RECOMMENDED GRAPH ?? (YES/NO): ")
    print(f"Best graph generated {graph}")

    if confirm.lower() == "yes" and graph is not None:
        if graph == "line plot":
            plt.plot(df[date[0]], df[numeric[0]], linewidth=1, color="cyan")
            plt.xlabel(date[0])
            plt.ylabel(numeric[0])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        elif graph == "Bar plot":
            plt.bar(df[catagory[0]], df[numeric[0]], width=1, color="cyan", edgecolor="red", linewidth=0.4)
            plt.xlabel(catagory[0])
            plt.ylabel(numeric[0])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        elif graph == "Histogram / Box plot":
            plt.subplot(1, 2, 1)
            plt.hist(df[numeric[0]], bins=10, color="cyan", edgecolor="red", linewidth=0.4)
            plt.xlabel(numeric[0])
            plt.ylabel("Frequency")
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.subplot(1, 2, 2)
            plt.boxplot(df[numeric[0]], vert=False)
            plt.xlabel(numeric[0])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        elif graph == "scatter plot":
            plt.scatter(df[numeric[0]], df[numeric[1]], color="cyan", edgecolor="red", linewidth=0.4)
            plt.xlabel(numeric[0])
            plt.ylabel(numeric[1])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        elif graph == "Pie chart":
            plt.pie(df[numeric[0]], labels=df[catagory[0]] if catagory else None, autopct="%1.1f%%", startangle=90, colors=["cyan", "gold"])
            plt.axis("equal")
            plt.title("Revenue over time")
            plt.show()
        elif graph == "scatter / line plot":
            plt.subplot(1, 2, 1)
            plt.scatter(df[numeric[0]], df[numeric[1]], color="cyan", edgecolor="red", linewidth=0.4)
            plt.xlabel(numeric[0])
            plt.ylabel(numeric[1])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.subplot(1, 2, 2)
            plt.plot(df[date[0]] if date else df.index, df[numeric[0]], linewidth=1, color="gold")
            plt.xlabel(date[0] if date else "index")
            plt.ylabel(numeric[0])
            plt.title("Revenue over time")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
    else:
        print("Opening Graph Studio...")
        print("Available Graphs:")
        print("1. Line Plot")
        print("2. Scatter Plot")
        print("3. Bar Plot")
        print("4. Histogram")
        print("5. Pie Chart")
        print("6. Box Plot")
        print("7. Stack Area Plot")
        print("8. Step Plot")
        print("9. Fill Between Plot")

        try:
            gchoice = int(input("Select a graph (1-9): "))
        except ValueError:
            print("Invalid choice")
            gchoice = 0
        print("Available columns:", df.columns.tolist())
        cols = input("Enter required columns (comma separated): ").split(",")
        cols = [c.strip() for c in cols]
        if len(df.columns) > 7:
            print("Too many columns. Suggesting important ones...")
            print("Ranking columns by usefulness (numeric first):")
            print(df.select_dtypes(include='number').columns.tolist())

        if len(df) > 400:
            print("Large dataset detected (greater than 400). Sampling intelligently...")
            df_sample = df.sample(400) if len(df) >= 400 else df.sample(len(df))
        else:
            df_sample = df

        # FIX: track the main plotted artist(s) so later customization
        # (color, alpha, marker, linestyle) can be applied to what was
        # actually drawn instead of silently doing nothing or duplicating
        # the plot.
        plotted_artists = []

        if gchoice == 1:  # Line Plot
            line, = plt.plot(df_sample[cols[0]], df_sample[cols[1]])
            plotted_artists = [line]
            plt.title("Line Plot")
        elif gchoice == 2:  # Scatter Plot
            sc = plt.scatter(df_sample[cols[0]], df_sample[cols[1]])
            plotted_artists = [sc]
            plt.title("Scatter Plot")
        elif gchoice == 3:  # Bar Plot
            bars = plt.bar(df_sample[cols[0]], df_sample[cols[1]])
            plotted_artists = list(bars)
            plt.title("Bar Plot")
        elif gchoice == 4:  # Histogram
            df_sample[cols[0]].plot(kind='hist', bins=20, title="Histogram")
        elif gchoice == 5:  # Pie Chart
            df_sample[cols[0]].value_counts().plot(kind='pie', autopct='%1.1f%%', title="Pie Chart")
        elif gchoice == 6:  # Box Plot
            df_sample[cols[0]].plot(kind='box', title="Box Plot")
        elif gchoice == 7:  # Stack Area Plot
            # FIX: area plot needs at least 2 numeric columns to be
            # meaningful and stacked -- guard against a single/invalid column
            if len(cols) >= 2:
                df_sample[cols].plot(kind='area', stacked=True, title="Stack Area Plot")
            else:
                print("Stack area plot needs at least 2 columns. Skipping.")
        elif gchoice == 8:  # Step Plot
            line, = plt.step(df_sample[cols[0]], df_sample[cols[1]])
            plotted_artists = [line]
            plt.title("Step Plot")
        elif gchoice == 9:  # Fill Between Plot
            plt.fill_between(df_sample.index, df_sample[cols[0]], df_sample[cols[1]], alpha=0.5)
            plt.title("Fill Between Plot")
        else:
            print("Invalid graph choice")

        plt.xlabel(cols[0])
        if len(cols) > 1:
            plt.ylabel(cols[1])
        plt.xticks(rotation=45)
        # FIX: legend() on plots with no labeled artists (pie/hist/box/area)
        # produces a warning or a meaningless legend -- only call it when
        # there's something it can actually label.
        if plotted_artists:
            plt.legend(cols, loc="best")
        plt.grid(True)
        plt.show()

        choice = input("CUSTOMISE GRAPH ?? (YES/NO)")
        if choice.lower() == "yes":
            title = input("Enter graph title: ")
            xlabel = input("Enter x-axis label: ")
            ylabel = input("Enter y-axis label: ")
            color = input("Enter line/bar color: ")
            transparency = input("Enter transparency (0-1): ")
            grid = input("Show grid? (yes/no): ")
            marker = input("Enter marker style (e.g., 'o', 's', '^'): ")
            line_style = input("Enter line style (e.g., '-', '--', '-.', ':'): ")
            rotate_labels = input("Rotate x-axis labels? (yes/no): ")
            add_legend = input("Add legend? (yes/no): ")
            text_labels = input("Add text labels? (yes/no): ")
            print()
            apply_customizations = input("Apply customizations? (yes/no): ")
            if apply_customizations.lower() == "yes":
                plt.title(title)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                # FIX: re-plot once with all chosen style options together
                # instead of calling plt.plot() multiple times (which was
                # stacking duplicate overlapping lines), and apply alpha to
                # the actual artist instead of the axes background patch.
                plot_kwargs = {}
                if color:
                    plot_kwargs["color"] = color
                if transparency:
                    try:
                        plot_kwargs["alpha"] = float(transparency)
                    except ValueError:
                        print("Invalid transparency value, skipping.")
                if marker:
                    plot_kwargs["marker"] = marker
                if line_style:
                    plot_kwargs["linestyle"] = line_style
                if plot_kwargs and len(cols) > 1:
                    plt.plot(df_sample[cols[0]], df_sample[cols[1]], **plot_kwargs)
                if grid.lower() == "yes":
                    plt.grid(True)
                else:
                    plt.grid(False)
                if rotate_labels.lower() == "yes":
                    plt.xticks(rotation=45)
                if add_legend.lower() == "yes":
                    plt.legend(cols, loc="best")
                if text_labels.lower() == "yes" and len(cols) > 1:
                    for i, txt in enumerate(df_sample[cols[1]]):
                        plt.annotate(txt, (df_sample[cols[0]].iloc[i], df_sample[cols[1]].iloc[i]))
                plt.show()
            else:
                print("Customizations not applied.")

            # FIX: colour_choice must always be defined before use --
            # previously it was only set inside this block's prompt and
            # would raise NameError below if "advanced customization" was
            # answered "no" at a point where colour_choice hadn't been
            # asked yet on this path.
            colour_choice = None
            choice = input("ADVANCED GRAPH CUSTOMIZATION? (yes/no): ")
            if choice.lower() == "yes":
                print('''choose the colour type:
                 1. Single Colour
                 2. Multiple colours''')
                colour_choice = input("Enter your choice (1 or 2): ")
                color = None
                random_color = None
                if colour_choice == "1":
                    color = input("Enter the colour: ")
                elif colour_choice == "2":
                    print("showing colour palette...")
                    colors = [
                        "red", "blue", "green", "orange",
                        "purple", "pink", "brown", "cyan",
                        "magenta", "yellow", "black"
                    ]
                    random_color = random.choice(colors)
                    print("Selected Color:", random_color)

                choice = input("apply advanced customisation? (yes/no): ")
                if choice.lower() == "yes":
                    print("Applying advanced customisation...")
                    # FIX: set_prop_cycle only affects artists plotted AFTER
                    # it's called -- it does nothing to the figure already
                    # shown. Re-plot with the chosen color so it's visible.
                    if colour_choice == "1" and color and len(cols) > 1:
                        plt.plot(df_sample[cols[0]], df_sample[cols[1]], color=color)
                    elif colour_choice == "2" and random_color and len(cols) > 1:
                        plt.plot(df_sample[cols[0]], df_sample[cols[1]], color=random_color)
                    plt.show()
                else:
                    print("Advanced customisation not applied.")

            choice = input("COMPARE COLOUMNS ?? (yes/no): ")
            if choice.lower() == "yes":
                col1 = input("Enter the first coloumn name: ")
                col2 = input("Enter the second coloumn name: ")
                if col1 in df.columns and col2 in df.columns:
                    plt.scatter(df[col1], df[col2])
                    plt.title(f"Comparison of {col1} and {col2}")
                    plt.xlabel(col1)
                    plt.ylabel(col2)
                    plt.grid(True)
                    plt.show()
                else:
                    print("Invalid coloumn names.")
            else:
                print("No comparison performed.")

            choice = input("HIGHLIGHT TOP VALUES ?? (yes/no): ")
            if choice.lower() == "yes":
                print("Highlighting maximum values")
                for col in df.select_dtypes(include='number').columns:
                    max_value = df[col].max()
                    plt.bar(df.index, df[col], color='lightblue')
                    plt.bar(df[df[col] == max_value].index, df[df[col] == max_value][col], color='red')
                    plt.title(f"Highlighting maximum values in {col}")
                    plt.xlabel("Index")
                    plt.ylabel(col)
                    plt.grid(True)
                    plt.show()
                print("Minimum values highlighted.")
                for col in df.select_dtypes(include='number').columns:
                    min_value = df[col].min()
                    plt.bar(df.index, df[col], color='lightblue')
                    plt.bar(df[df[col] == min_value].index, df[df[col] == min_value][col], color='green')
                    plt.title(f"Highlighting minimum values in {col}")
                    plt.xlabel("Index")
                    plt.ylabel(col)
                    plt.grid(True)
                    plt.show()
                print("highlighting outliers....")
                for col in df.select_dtypes(include='number').columns:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                    plt.scatter(df.index, df[col], color='lightblue')
                    plt.scatter(outliers.index, outliers[col], color='orange')
                    plt.title(f"Highlighting outliers in {col}")
                    plt.xlabel("Index")
                    plt.ylabel(col)
                    plt.grid(True)
                    plt.show()
            else:
                print("No highlighting performed.")

            print("INSIGHTS GENERATED SUCCESSFULLY.......")
            print(f"Highest value in the dataset: {df.max(numeric_only=True).max()}")
            print(f"Lowest value in the dataset: {df.min(numeric_only=True).min()}")
            print(f"average value in the dataset: {df.mean(numeric_only=True).mean()}")
            print(f"median value in the dataset: {df.median(numeric_only=True).median()}")
            print(f"standard deviation in the dataset: {df.std(numeric_only=True).std()}")
            print(f"variance in the dataset: {df.var(numeric_only=True).var()}")
            # FIX: df.mode().mode() calls mode() on a dataframe of modes,
            # which is logically wrong and can raise/produce nonsense.
            # df.mode() already gives the per-column mode(s); use that once.
            modes = df.mode()
            print(f"mode in the dataset: {modes.values}")
            print(f"top category in the dataset: {modes.values}")
            print(f"bottom category in the dataset: {modes.values}")
            print(f"strongest trend in the dataset: {df.corr(numeric_only=True).max().max()}")

            choice = input("GENERATE REPORT?? (yes/no): ")
            if choice.lower() == "yes":
                print("Statistical report generated successfully...")

total_graphs_generated = 0
total_insights_generated = 0
exported_files = []

choice = input("GENERATE DASHBOARD ?? (yes/no): ")
if choice.lower() == "yes":
    print("_____________________________________________________________________")
    numeric = df.select_dtypes(include="number").columns.tolist()
    catagory = df.select_dtypes(include="object").columns.tolist()
    date = df.select_dtypes(include="datetime").columns.tolist()

    print("Creating subplot layout...")
    plt.figure(figsize=(14, 10))

    print("Generating Key Metric Chart...")
    plt.subplot(2, 3, 1)
    if numeric:
        plt.bar(["Min", "Mean", "Max"], [df[numeric[0]].min(), df[numeric[0]].mean(), df[numeric[0]].max()], color="cyan")
        plt.title(f"Key Metric: {numeric[0]}")
    else:
        plt.title("Key Metric (no numeric coloumn)")

    print("Generating Distribution Chart...")
    plt.subplot(2, 3, 2)
    if numeric:
        plt.hist(df[numeric[0]], bins=10, color="cyan", edgecolor="red", linewidth=0.4)
        plt.title(f"Distribution: {numeric[0]}")
    else:
        plt.title("Distribution (no numeric coloumn)")

    print("Generating Category Chart...")
    plt.subplot(2, 3, 3)
    if catagory:
        df[catagory[0]].value_counts().plot(kind="bar", color="gold")
        plt.title(f"Category: {catagory[0]}")
        plt.xticks(rotation=45)
    else:
        plt.title("Category (no categorical coloumn)")

    print("Generating Trend Chart...")
    plt.subplot(2, 3, 4)
    if date and numeric:
        plt.plot(df[date[0]], df[numeric[0]], color="cyan")
        plt.title(f"Trend: {numeric[0]} over {date[0]}")
        plt.xticks(rotation=45)
    elif numeric:
        plt.plot(df.index, df[numeric[0]], color="cyan")
        plt.title(f"Trend: {numeric[0]} over index")
    else:
        plt.title("Trend (no numeric coloumn)")

    print("Generating Summary Section...")
    plt.subplot(2, 3, 5)
    plt.axis("off")
    summary_text = f"Rows: {len(df.index)}\nColoumns: {len(df.columns)}\nMissing values: {df.isnull().sum().sum()}\nDublicate rows: {df.duplicated().sum()}"
    plt.text(0.1, 0.5, summary_text, fontsize=10)
    plt.title("Summary")

    plt.tight_layout()
    print("Displaying complete dashboard...")
    plt.show()
    total_graphs_generated += 1
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

choice = input("ASK YOUR DATA ?? (yes/no): ")
if choice.lower() == "yes":
    print("_____________________________________________________________________")
    print("Example: Show top 5 products")
    print("Example: Show city wise sales")
    print("Example: Show average marks")
    query = input("Enter your query: ").strip().lower()

    numeric = df.select_dtypes(include="number").columns.tolist()
    catagory = df.select_dtypes(include="object").columns.tolist()

    if "top" in query:
        words = query.split()
        n = 5
        for w in words:
            if w.isdigit():
                n = int(w)
        target = numeric[0] if numeric else None
        for col in numeric:
            if col.lower() in query:
                target = col
        if target:
            print(f"Top {n} rows by {target}:")
            print(df.sort_values(by=target, ascending=False).head(n))
        else:
            print("No numeric coloumn found to sort by.")
    elif "wise" in query:
        group_col = None
        for col in catagory:
            if col.lower() in query:
                group_col = col
        value_col = numeric[0] if numeric else None
        for col in numeric:
            if col.lower() in query:
                value_col = col
        if group_col and value_col:
            print(f"{value_col} grouped by {group_col}:")
            print(df.groupby(group_col)[value_col].sum())
        else:
            print("Could not find matching coloumns for this query.")
    elif "average" in query or "mean" in query:
        target = numeric[0] if numeric else None
        for col in numeric:
            if col.lower() in query:
                target = col
        if target:
            print(f"Average {target}: {df[target].mean()}")
        else:
            print("No numeric coloumn found to average.")
    else:
        print("Sorry, could not understand the query.")
    total_insights_generated += 1
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

choice = input("GENERATE REPORT ?? (yes/no): ")
if choice.lower() == "yes":
    print("_____________________________________________________________________")
    print("Creating Statistical Report...")
    print(df.describe())
    print("Creating Graph Report...")
    print(f"Total graphs generated so far: {total_graphs_generated}")
    print("Creating Insight Report...")
    print(f"Highest value in the dataset: {df.max(numeric_only=True).max()}")
    print(f"Lowest value in the dataset: {df.min(numeric_only=True).min()}")
    print(f"Average value in the dataset: {df.mean(numeric_only=True).mean()}")
    total_insights_generated += 1
    print("Combining results...")
    print("Generating final report...")
    print("Report generated successfully.")
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

choice = input("SAVE OUTPUT ?? (yes/no): ")
if choice.lower() == "yes":
    print("_____________________________________________________________________")
    output_folder = os.path.dirname(os.path.abspath(path))

    c = input("Export Graph as PNG ?? (yes/no): ")
    if c.lower() == "yes":
        numeric = df.select_dtypes(include="number").columns.tolist()
        if numeric:
            graph_path = os.path.join(output_folder, "graph_output.png")
            plt.hist(df[numeric[0]], bins=10, color="cyan", edgecolor="red", linewidth=0.4)
            plt.title(f"Distribution of {numeric[0]}")
            plt.savefig(graph_path)
            plt.close()
            exported_files.append(graph_path)
            total_graphs_generated += 1
            print(f"Graph saved to {graph_path}")
        else:
            print("No numeric coloumn found.")

    c = input("Export Dashboard as PNG ?? (yes/no): ")
    if c.lower() == "yes":
        dashboard_path = os.path.join(output_folder, "dashboard_output.png")
        numeric = df.select_dtypes(include="number").columns.tolist()
        catagory = df.select_dtypes(include="object").columns.tolist()
        plt.figure(figsize=(14, 10))
        plt.subplot(2, 2, 1)
        if numeric:
            plt.hist(df[numeric[0]], bins=10, color="cyan")
            plt.title(f"Distribution: {numeric[0]}")
        plt.subplot(2, 2, 2)
        if catagory:
            df[catagory[0]].value_counts().plot(kind="bar", color="gold")
            plt.title(f"Category: {catagory[0]}")
        plt.subplot(2, 2, 3)
        if numeric:
            plt.plot(df.index, df[numeric[0]], color="cyan")
            plt.title(f"Trend: {numeric[0]}")
        plt.tight_layout()
        plt.savefig(dashboard_path)
        plt.close()
        exported_files.append(dashboard_path)
        total_graphs_generated += 1
        print(f"Dashboard saved to {dashboard_path}")

    c = input("Export Report as PDF ?? (yes/no): ")
    if c.lower() == "yes":
        report_path = os.path.join(output_folder, "report_output.pdf")
        plt.figure(figsize=(8.5, 11))
        plt.axis("off")
        report_text = f"STATISTICAL REPORT\n\n{df.describe()}\n\nTotal graphs generated: {total_graphs_generated}\nTotal insights generated: {total_insights_generated}"
        plt.text(0.05, 0.95, report_text, fontsize=8, va="top", family="monospace")
        plt.savefig(report_path)
        plt.close()
        exported_files.append(report_path)
        print(f"Report saved to {report_path}")

    c = input("Export Cleaned Dataset as CSV ?? (yes/no): ")
    if c.lower() == "yes":
        csv_path = os.path.join(output_folder, "cleaned_dataset.csv")
        df.to_csv(csv_path, index=False)
        exported_files.append(csv_path)
        print(f"Cleaned dataset saved to {csv_path}")

    c = input("Export Cleaned Dataset as Excel ?? (yes/no): ")
    if c.lower() == "yes":
        excel_path = os.path.join(output_folder, "cleaned_dataset.xlsx")
        df.to_excel(excel_path, index=False)
        exported_files.append(excel_path)
        print(f"Cleaned dataset saved to {excel_path}")

    print("Export completed successfully.")
    print("_____________________________________________________________________")
else:
    print("THANK YOU")

print("_____________________________________________________________________")
print("SESSION SUMMARY")
print(f"Total graphs generated: {total_graphs_generated}")
print(f"Total insights generated: {total_insights_generated}")
print(f"File export details: {exported_files}")
print("_____________________________________________________________________")
print("Thank you for using the tool!")
