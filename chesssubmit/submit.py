# submit.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess results source document validation application."""

if __name__ == "__main__":

    from . import APPLICATION_NAME

    try:
        from solentware_misc.gui.startstop import (
            start_application_exception,
            stop_application,
            application_exception,
        )
    except Exception as error:
        import tkinter.messagebox

        try:
            tkinter.messagebox.showerror(
                title="Start Exception",
                message=".\n\nThe reported exception is:\n\n".join(
                    (
                        " ".join(
                            (
                                "Unable to import",
                                "solentware_misc.gui.startstop module",
                            )
                        ),
                        str(error),
                    )
                ),
            )
        except tkinter.TclError:
            pass
        raise SystemExit(
            "Unable to import start application utilities"
        ) from error
    try:
        from .gui.resultsroot import Results
        from .gui.leagues_submit import Leagues
    except Exception as error:
        start_application_exception(
            error, appname=APPLICATION_NAME, action="import"
        )
        raise SystemExit(
            " import ".join(("Unable to", APPLICATION_NAME))
        ) from error
    try:
        app = Results(
            title=APPLICATION_NAME, gui_module=Leagues, width=400, height=200
        )
    except Exception as error:
        start_application_exception(
            error, appname=APPLICATION_NAME, action="initialise"
        )
        raise SystemExit(
            " initialise ".join(("Unable to", APPLICATION_NAME))
        ) from error
    try:
        app.root.mainloop()
    except SystemExit:
        stop_application(app, app.root)
        raise
    except Exception as error:
        application_exception(
            error,
            app,
            app.root,
            title=APPLICATION_NAME,
            appname=APPLICATION_NAME,
        )
        raise SystemExit(
            " reporting exception in ".join(
                ("Exception while", APPLICATION_NAME)
            )
        ) from error
