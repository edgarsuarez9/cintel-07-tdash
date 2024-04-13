import seaborn as sns
from faicons import icon_svg # importing icon_svg for icons
from shinyswatch import theme # imports theme from shinyswatch to allow for appearance changes
from shiny import reactive # importing reactive from shiny
from shiny.express import input, render, ui # importing components from shiny
import palmerpenguins # importing pendguin data set

theme.united() # adjusts color and appearance

# loading palmer penguins data set 
df = palmerpenguins.load_penguins() 

#Page options and setting up title
ui.page_opts(title="Penguins dashboard", fillable=True)

# creating a sidebar for inputs
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    ) # adding hyperlink
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    ) # adding hyperlink
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    ) # adding hyperlink
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#creating a layout to display outputs 
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")): # including value box 
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True): # adding a card to present scatterplot 
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


# reactive function to filter data frame based on inputs
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

@reactive.effect
def _():
    if input.dark_mode() == "Yes":
        ui.update_dark_mode("dark")
    else:
        ui.update_dark_mode("light")
