import dash_mantine_components as dmc
from dash import dcc
from dash_iconify import DashIconify


def get_icon(icon):
    return DashIconify(icon=icon, height=20)


def layout():
    steps = [
        dmc.StepperStep(
            label="Calibration",
            description="Experimental Setup",
            # icon=get_icon(icon="material-symbols:account-circle"),
            # progressIcon=get_icon(icon="material-symbols:account-circle"),
            # completedIcon=get_icon(icon="mdi:account-check"),
            children=[
                dmc.Text(
                    "Step 1: Set mask and detector setup and"
                    + " other experimental parameters.",
                    align="center",
                )
            ],
        ),
        dmc.StepperStep(
            label="Reductions",
            description="Transformation and Reductions to 1D",
            # icon=get_icon(icon="ic:outline-email"),
            # progressIcon=get_icon(icon="ic:outline-email"),
            # completedIcon=get_icon(
            #    icon="material-symbols:mark-email-read-rounded"
            # ),
            children=[
                dmc.Text(
                    "Step 2: Set parameters for reduction extracts",
                    align="center",
                )
            ],
        ),
        dmc.StepperStep(
            label="Feature Extraction",
            description="Peak Detection and Curve Fitting",
            # icon=get_icon(icon="material-symbols:lock-outline"),
            # progressIcon=get_icon(icon="material-symbols:lock-outline"),
            # completedIcon=get_icon(
            #    icon="material-symbols:lock-open-outline"
            # ),
            children=[
                dmc.Text(
                    "Step 3: Set parameters to extract peaks",
                    align="center",
                )
            ],
        ),
        dmc.StepperStep(
            label="Optimization",
            description="Objective from Features",
            # icon=get_icon(icon="material-symbols:lock-outline"),
            # progressIcon=get_icon(icon="material-symbols:lock-outline"),
            # completedIcon=get_icon(
            #    icon="material-symbols:lock-open-outline"
            # ),
            children=[
                dmc.Text(
                    "Step 4: Set parameters for experiment objective",
                    align="center",
                )
            ],
        ),
        dmc.StepperCompleted(
            children=[
                dmc.Text(
                    "Workflow Setup completed, click back button to get to"
                    + "previous step",
                    align="center",
                )
            ]
        ),
    ]

    stepper_buttons = dmc.Group(
        position="center",
        mt="xl",
        children=[
            dmc.Button("Back", id="progress-back", variant="default"),
            dmc.Button("Next step", id="progress-next"),
            dcc.Store("progress-min-step", data=0),
            dcc.Store("progress-max-step", data=4),
        ],
    )

    return dmc.Container(
        [
            dmc.Stepper(
                id="progress-stepper",
                active=1,
                breakpoint="sm",
                orientation="horizontal",
                children=steps,
            ),
            stepper_buttons,
        ]
    )
