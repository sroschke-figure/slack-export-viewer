import os

import flask
from flask import current_app

app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

#app.app_context()

def read_css_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

@app.route("/channel/<name>/")
def channel_name(name):
    messages = current_app.channels[name]
    channels = list(current_app.channels.keys())
    groups = list(current_app.groups.keys()) if current_app.groups else {}
    dm_users = list(current_app.dm_users)
    mpim_users = list(current_app.mpim_users)

    viewer_css_contents = read_css_file(os.path.join(app.static_folder, 'viewer.css')) if app.no_external_references else None

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups) if groups else {},
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references,
                                 viewer_css_contents=viewer_css_contents)


@app.route("/channel/<name>/attachments/<attachment>")
def channel_name_attachment(name, attachment):
    return flask.send_file(os.path.join(current_app.path, name, "attachments", attachment))


@app.route("/group/<name>/")
def group_name(name):
    messages = current_app.groups[name]
    channels = list(current_app.channels.keys())
    groups = list(current_app.groups.keys())
    dm_users = list(current_app.dm_users)
    mpim_users = list(current_app.mpim_users)

    viewer_css_contents = read_css_file(os.path.join(app.static_folder, 'viewer.css')) if app.no_external_references else None

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references,
                                 viewer_css_contents=viewer_css_contents)


@app.route("/group/<name>/attachments/<attachment>")
def group_name_attachment(name, attachment):
    return flask.send_file(os.path.join(current_app.path, name, "attachments", attachment))


@app.route("/dm/<id>/")
def dm_id(id):
    messages = current_app.dms[id]
    channels = list(current_app.channels.keys())
    groups = list(current_app.groups.keys())
    dm_users = list(current_app.dm_users)
    mpim_users = list(current_app.mpim_users)

    viewer_css_contents = read_css_file(os.path.join(app.static_folder, 'viewer.css')) if app.no_external_references else None

    return flask.render_template("viewer.html", messages=messages,
                                 id=id.format(id=id),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references,
                                 viewer_css_contents=viewer_css_contents)


@app.route("/dm/<name>/attachments/<attachment>")
def dm_name_attachment(name, attachment):
    return flask.send_file(os.path.join(current_app.path, name, "attachments", attachment))


@app.route("/mpim/<name>/")
def mpim_name(name):
    messages = current_app.mpims.get(name, list())
    channels = list(current_app.channels.keys())
    groups = list(current_app.groups.keys())
    dm_users = list(current_app.dm_users)
    mpim_users = list(current_app.mpim_users)

    viewer_css_contents = read_css_file(os.path.join(app.static_folder, 'viewer.css')) if app.no_external_references else None

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references,
                                 viewer_css_contents=viewer_css_contents)


@app.route("/mpim/<name>/attachments/<attachment>")
def mpim_name_attachment(name, attachment):
    return flask.send_file(os.path.join(current_app.path, name, "attachments", attachment))


@app.route("/")
def index():
    channels = list(current_app.channels.keys())
    groups = list(current_app.groups.keys())
    dms = list(current_app.dms.keys())
    mpims = list(current_app.mpims.keys())
    if channels:
        if "general" in channels:
            return channel_name("general")
        else:
            return channel_name(channels[0])
    elif groups:
        return group_name(groups[0])
    elif dms:
        return dm_id(dms[0])
    elif mpims:
        return mpim_name(mpims[0])
    else:
        return "No content was found in your export that we could render."

