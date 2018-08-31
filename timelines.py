#!/usr/bin/python3

import svgwrite
from datetime import datetime

svg_x = 1000
svg_y = 225
svg_x_mid = svg_x / 2.0
svg_y_mid = 150

color_gray_light = "#b3b3b3"
color_gray_dark = "#3c3c3e"
color_green = "#43c200"
color_purple = "#5c3dcc"
color_orange = "#e3673e"
color_blue = "#40D8D9"
color_red = "#FF0900"

color_list = [color_green, color_orange, color_blue, color_red]

line_width = 8
line_color = color_purple
line_style = ""
line_border_margin = 80
line_x1 = line_border_margin / 2.0
line_x2 = svg_x - line_border_margin
line_len = svg_x - line_x1 - (svg_x - line_x2)
line_grade_height = 15

grade_width = line_width * 0.7
grade_height = line_grade_height * 0.7

text_angle = -25

label_margin = 40
peg_margin = 20
label_x_pos_prev = 0
peg_x_pos_prev = 0


def addTextAngle(svg_document, text, angle, pos_x, pos_y, font_sz=21, color=color_gray_dark):
    print("addTextAngle color: {}".format(color))
    text = svg_document.text(
        text,
        insert = (pos_x, pos_y),
        style = "fill: {}; font-size: {}px; font-weight: bold; font-family: Liberation Sans;".format(color, font_sz),
        text_anchor = "start"
    )

    textGroup = svgwrite.container.Group(
        transform = "rotate(%d, %s, %s)" % (angle, pos_x, pos_y)
    )
    textGroup.add(text)
    svg_document.add(textGroup)

def writeTimelineBase(svg_document, span):
    svg_document.add(svg_document.line(start = (line_x1, svg_y_mid),
                                       end   = (line_x2, svg_y_mid),
                                       stroke_width = line_width,
                                       stroke = line_color,
                                       stroke_linecap = "round"))
    svg_document.add(svg_document.line(start = (line_x1, svg_y_mid - line_grade_height),
                                       end   = (line_x1, svg_y_mid + line_grade_height),
                                       stroke_width = line_width,
                                       stroke = line_color,
                                       stroke_linecap = "round"))
    svg_document.add(svg_document.line(start = (line_x2, svg_y_mid - line_grade_height),
                                       end   = (line_x2, svg_y_mid + line_grade_height),
                                       stroke_width = line_width,
                                       stroke = line_color,
                                       stroke_linecap = "round"))

    addTextAngle(svg_document, span[0], -90, line_x1-13, svg_y_mid - line_grade_height + 38)
    addTextAngle(svg_document, span[1], -90, line_x2+27, svg_y_mid - line_grade_height + 38)
    label_x_pos_prev = line_x1
    peg_x_pos_prev = line_x1

    year_start = int(span[0])
    year_end = int(span[1])
    nbr_grades = year_end - year_start

    if nbr_grades < 2:
        return

    for pos in range(0, nbr_grades):
        x_pos = line_x1 + (line_len/nbr_grades) * pos
        line = svg_document.line(start = (x_pos, svg_y_mid - grade_height),
                                 end   = (x_pos, svg_y_mid + grade_height),
                                 stroke_width = grade_width,
                                 stroke = line_color,
                                 stroke_linecap = "round")
        svg_document.add(line)


def writeTimelineItem(svg_document, span, item, color):
    print("writeTimelineItem: Item: {}".format(item))

    item_time = item[0]
    span_start = int(span[0])
    span_end = int(span[1])
    item_year = int(item_time.split("-")[0])
    item_month = int(item_time.split("-")[1])

    if item_year < span_start:
        return



    nbr_years =  span_end - span_start
    month_span = nbr_years * 12;

    month_idx = (item_year-span_start) * 12 + item_month - 1

    month_pos = (1.0/(1.0*month_span)) * month_idx
    x_offset = month_pos * line_len
    item_x_pos = line_x1 + x_offset

    global label_x_pos_prev
    global peg_x_pos_prev

    label_x_pos = item_x_pos
    if label_x_pos - label_x_pos_prev < label_margin:
        label_x_pos = label_x_pos_prev + label_margin

    peg_x_pos = item_x_pos
    if peg_x_pos - peg_x_pos_prev < peg_margin:
        peg_x_pos = peg_x_pos_prev + peg_margin

    label_x_pos_prev = label_x_pos
    peg_x_pos_prev = peg_x_pos

    print("writeTimelineItem: Year: {}, Month: {}, Monthspan: {}, Monthidx: {}, item_x_pos: {}".format(item_year, item_month, month_span, month_idx, item_x_pos))

    svg_document.add(svg_document.line(start = (peg_x_pos, svg_y_mid - line_grade_height*1.1),
                                       end   = (peg_x_pos, svg_y_mid),
                                       stroke_width = grade_width,
                                       stroke = color,
                                       stroke_linecap = "round"))
    y_margin = 20
    addTextAngle(svg_document, item[2], text_angle, label_x_pos, svg_y_mid - y_margin - 3)


def writeTimelineProject(svg_document, span, project, project_nbr, color):
    print("writeTimelineProject: Project #{}, color: {} - {}".format(project_nbr, color, project))

    global label_x_pos_prev
    global peg_x_pos_prev
    label_x_pos_prev = line_x1
    peg_x_pos_prev = line_x1

    for item in project[1]:
        writeTimelineItem(svg_document, span, item, color)

def writeTimelineVendor(span, vendor):
    print("Span: {}".format(span))
    print("Vendor: {}".format(vendor))

    vendor_name = vendor[0]
    vendor_projects = vendor[1]
    print("Vendor name: {}".format(vendor_name))
    print("Vendor projects: {}".format(vendor_projects))

    for project in vendor_projects:
        project_name = project[0]
        project_events = project[1]

        # If timeline has no events, don't create the file
        if (len(project_events) == 0):
            continue

        filename = "timeline_{}_{}.svg".format(vendor_name.lower(), project_name.lower().replace(" ", "_"))
        print("Output file: {}".format(filename))
        svg_document = svgwrite.Drawing(filename = filename,
                                        size = (svg_x, svg_y))

        project_nbr = vendor_projects.index(project)
        color_idx = min(project_nbr, len(color_list) - 1)
        color = color_list[color_idx]

        writeTimelineProject(svg_document, span, project, project_nbr, color)
        writeTimelineBase(svg_document, span)
        addTextAngle(svg_document, project_name, 0, line_x1 - 5, svg_y_mid + 3.5*line_grade_height, font_sz=28)

        print("\n{}\n\n".format(svg_document.tostring()))
        svg_document.save()

def getEntryInt(entry):
    date = entry[0]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = 0
    try:
        day = int(date.split('-')[2])
    except IndexError:
        pass
    dateInt = year*12*31 + month*31 + day
    print("getEntryInt() {} {} - {}".format(entry[2],entry[0], dateInt))
    return dateInt

def firstEntry(entryA, entryB):
    dateIntA = getEntryInt(entryA)
    dateIntB = getEntryInt(entryB)
    if dateIntA < dateIntB:
        return entryA
    else:
        return entryB

def combineTimelines(vendor, projectA, projectB, projectName):
    timelines = dict()
    projectAEntry = None
    projectBEntry = None

    for project in vendor[1]:
        if project[0] == projectA:
            projectAEntry = project
            timelines[projectA] = project[1]
            print("combineTimelines() Found {} project in vendor {}".format(projectA, vendor[0]))
        if project[0] == projectB:
            projectBEntry = project
            timelines[projectB] = project[1]
            print("combineTimelines() Found {} project in vendor {}".format(projectB, vendor[0]))

    print("combineTimelines() found {} matching timelines".format(len(timelines)))
    if len(timelines) != 2:
        # If we havent found project A & B
        return None

    entrySet = set()
    for entry in timelines[projectA] + timelines[projectB]:
        entrySet.add(entry[2])

    newProjectEntries = []
    for entry in entrySet:
        print("Looking for \'{}\'".format(entry))
        newEntry = ("9999-9999", "N/A", entry)
        for entryA in timelines[projectA]:
            if entry == entryA[2]:
                # We've found an with the same descr
                newEntry = firstEntry(newEntry, entryA)
        for entryB in timelines[projectB]:
            if entry == entryB[2]:
                newEntry = firstEntry(newEntry, entryB)
        newEntry = (newEntry[0], "N/A", newEntry[2])
        print("NewEntry: {}".format(newEntry))
        newProjectEntries.append(newEntry)

    newProjectEntries.sort(key=getEntryInt)
    newProject = (projectName, newProjectEntries)
    retval = newProject
    print("*****\nNew Project: {}*****\n\n".format(vendor, retval))
    return retval

#### TODO: Write some code to combine kernel and mesa timelines


def createCombinedTimelines(timelines):
    newTimelines = []
    for vendor in timelines:
        newProject = combineTimelines(vendor, "Kernel", "Mesa", "Kernel and Mesa")
        if newProject != None:
            print("Added combined project")
            vendor[1].append(newProject)
            print("*****\nNew Project: {}*****\n\n".format(vendor))

        else:
            print("Did not add combined project")
        newTimelines.append(vendor)

    return newTimelines


def writeTimelines(timelines):
    span = ["2009", "2019"]

    for vendor in timelines:
        writeTimelineVendor(span, vendor)


timelines = [
    ("AMD", [
                ("Kernel", [
                    ("2009-06", "radeon", "r600"),
                    ("2010-01", "radeon", "Evergreen"),
                    ("2011-01", "radeon", "Northern Islands"),
                    ("2012-03", "radeon", "Southern Islands"),
                    ("2013-06", "radeon", "Sea Islands"),
                    ("2016-03", "amdgpu", "Polaris 10 & 11"),
                    ("2016-11", "amdgpu", "Vega 10"),
                    ("2016-12-14", "amdgpu", "Polaris 12"),
                    ("2017-09-26", "amdgpu", "Vega 12"),
                ]),
                ("Mesa", [
                    ("2010-05", "r600", "r600"),
                    ("2010-08", "r600", "Evergreen"),
                    ("2011-01", "r600", "Northern Islands"),
                    ("2012-01", "radeonsi", "Southern Islands"),
                    ("2013-10", "radeonsi", "Sea Islands"),
                    ("2015-11", "radeonsi", "Polaris 10 & 11"),
                    ("2016-12", "radeonsi", "Polaris 12"),
                    ("2016-12", "radeonsi", "Vega 10"),
                    ("2018-03-28", "radeonsi", "Vega 12"),
                    ("2018-07-12", "radeonsi", "Vega 20"),

                ]),
        ]
    ),
    ("ARM", [
                ("Kernel", [
                    ("2018-05-14", "lima", "Mali-4xx driver created"), # https://gitlab.freedesktop.org/lima/linux/commit/ac9d3fa76c365fe89b6cf3bdfda42fe84bd299e2
                ]),

                ("Mesa", [
                    ("2017-06-09", "lima", "Mali-4xx driver created"), # https://gitlab.freedesktop.org/lima/mesa/commit/be6749c1f3785300fafdba65264671af0a5f4aa7
                ]),
                ("Reverse Engineering", [
                    ("2012-02", "lima", "Mali-2/4xx prototyping"), # Luc Verhaegen https://www.youtube.com/watch?v=MvRJ_8K8baI
                    ("2017-06", "panfrost", "Gxx Shader Loader"),
                    ("2017-06-09", "lima", "Mali-4xx driver"), # https://gitlab.freedesktop.org/lima/mesa/commit/be6749c1f3785300fafdba65264671af0a5f4aa7
                    ("2018-02", "panfrost", "T7xx Initial 3D"),
                ]),
        ]
    ),
    ("Broadcom", [
                ("Kernel", [
                    ("2015-03", "vc4", "VC4"),
                    ("2018-04-30", "v3d", "V3D"),

                ]),

                ("Mesa", [
                    ("2014-06", "vc4", "VC4"),
                    ("2018-02-02", "vc5", "VC5"),
                    ("2018-05-01", "v3d", "VC5"),
                ]),
                ("Reverse Engineering", [

                ]),
        ]
    ),
    ("Imagination", [
                ("Kernel", [

                ]),

                ("Mesa", [

                ]),
                ("Reverse Engineering", [

                ]),
        ]
    ),
    ("Intel", [
                ("Kernel", [
                    ("2009-09", "i915", "Gen6 Sandy Bridge"),
                    ("2011-04", "i915", "Gen7 Ivy Bridge"),
                    ("2013-02", "i915", "Gen9 Skylake"),
                    ("2013-11", "i915", "Gen8 Broadwell"),
                    ("2017-06", "i915", "Gen10 Cannonlake"),
                    ("2018-02-15", "i915", "Gen11 Ice Lake"),
                ]),

                ("Mesa", [
                    ("2009-11", "i915", "Gen6 Sandy Bridge"),
                    ("2011-05", "i915", "Gen7 Ivy Bridge"),
                    ("2013-02", "i915", "Gen9 Skylake"),
                    ("2013-11", "i915", "Gen8 Broadwell"),
                    ("2017-05", "i915", "Gen10 Cannonlake"),
                    ("2018-03-02", "i915", "Gen11 Ice Lake"),
                ]),
                ("Reverse Engineering", [

                ]),
        ]
    ),
    ("NVidia", [
                ("Kernel", [
                    ("2009-11", "nouveau", "Driver added"),
                    ("2010-09", "nouveau", "Fermi"),
                    ("2012-03", "nouveau", "Kepler"),
                    ("2014-02", "nouveau", "Maxwell"),
                    ("2016-11", "nouveau", "Pascal"),
                    ("2018-05", "nouveau", "Volta"),
                ]),

                ("Mesa", [
                    ("2010-11", "nouveau", "Fermi"),
                    ("2012-04", "nouveau", "Kepler"),
                    ("2014-07", "nouveau", "Maxwell"),
                    ("2016-07", "nouveau", "Pascal"),
                ]),

                ("Reverse Engineering", [
                    ("2010-04", "envytools", "Fermi"),
                    ("2012-03", "envytools", "Kepler"),
                    ("2012-03", "grate", "Tegra"), # https://github.com/grate-driver/grate/commit/5386da0e6dee8840cf0441ffe2c9ec916f243350
                    ("2014-06", "envytools", "Maxwell"),
                    ("2016-06", "envytools", "Pascal"),
                    ("2018-03-30", "envytools", "Pascal"),

                ]),
        ]
    ),
    ("Qualcomm", [
                ("Kernel", [
                    ("2013-06", "msm", "Driver added"),
                    ("2013-06", "msm", "A200"),
                    ("2013-07", "msm", "A300"),
                    ("2014-09", "msm", "A400"),
                    ("2016-11", "msm", "A500"),
                    ("2018-08-06", "msm", "A600"),
                ]),

                ("Mesa", [
                    ("2012-10-01", "freedreno", "Driver added"),
                    ("2012-10-02", "freedreno", "A200"),
                    ("2013-05", "freedreno", "A300"),
                    ("2014-07", "freedreno", "A400"),
                    ("2016-11", "freedreno", "A500"),
                ]),
                ("Reverse Engineering", [
                    ("2013-03", "envytools", "A200/A300"),
                    ("2013-11", "envytools", "A400"),
                    ("2016-04", "envytools", "A500"),
                ]),
        ]
    ),
    ("Vivante", [
                ("Kernel", [
                    ("2015-12", "etnaviv", "Driver added"),
                    ("2015-12-03", "etnaviv", "GC2000"),
                    ("2016-01", "etnaviv", "GC3000"),
                    ("2018-01-22", "etnaviv", "GC7000"),
                ]),

                ("Mesa", [
                    ("2016-12", "etnaviv", "Driver added"),
                    ("2016-12", "etnaviv", "GC2000"),
                    ("2016-12", "etnaviv", "GC3000"),
                    ("2017-11", "etnaviv", "GC7000"),
                ]),
                ("Reverse Engineering", [
                    ("2012-12", "etna_viv", "Initial commit"),
                    ("2013-03", "etna_viv", "GC2000"),
                    ("2016-01", "etna_viv", "GC3000"),
                    ("2017-10", "etna_viv", "GC7000"),
                ]),
        ]
    ),

    ("imx8qm", [
                ("i.MX 8 Kernel", [
                    ("2016-11-30", "imx8",   "i.MX8 LPI2C support"),
                    ("2018-03-28", "imx8qm", "i.MX8 SATA support"),
                ]),
                ("i.MX 8 U-Boot", [
                    ("2018-01-10", "imx8m", "Initial support"),
                    ("2018-01-10", "imx8m", "Network Support"),
                    ("2018-01-10", "imx8m", "GPIO Support"),
                ]),
        ]
    ),
]


def main():
    global timelines
    timelines = createCombinedTimelines(timelines)
    writeTimelines(timelines)


if __name__ == "__main__":
    main()
