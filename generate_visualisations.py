import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import mpl_toolkits.axes_grid1.inset_locator as il
import csv

def split_lists(x_list, y_list, p1, p2):
    min_y = None
    max_y = None
    x_lists = [[],[],[]]
    y_lists = [[],[],[]]
    for y in y_list:
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y
    yp1 = min_y + (max_y - min_y)*p1
    yp2 = min_y + (max_y - min_y)*p2
    last_y = None
    for i, y in enumerate(y_list):
        if y <= yp1:
            x_lists[0].append(x_list[i])
            y_lists[0].append(y)
        elif y <= yp2:
            if last_y is not None:
                if last_y <= yp1:
                    x_lists[0].append(x_list[i])
                    y_lists[0].append(y)
            x_lists[1].append(x_list[i])
            y_lists[1].append(y)
        else:
            if last_y is not None:
                if last_y <= yp2:
                    x_lists[1].append(x_list[i])
                    y_lists[1].append(y)
            x_lists[2].append(x_list[i])
            y_lists[2].append(y)
        last_y = y

    return x_lists, y_lists

def perc_to_float(p):
    return float(p.strip('%'))/100

def generate_fig_1():
    sf = shapefile.Reader('SA4_2021_AUST_SHP_GDA2020/SA4_2021_AUST_GDA2020')
    csvf = open('covidData/vaccinations_by_sa4.csv', 'r')

    cf = csv.reader(csvf)

    nsw_vac_rates = {}

    for line in cf:
        if line[0] == 'NSW':
            nsw_vac_rates[line[1]] = [line[2],line[3]]

    colours = {0:'#756bb1',
               1:'#bcbddc',
               2:'#efedf5'}

    plt.clf()
    fig, ax = plt.subplots(figsize=(15,10), dpi=100)
    
    ax.set_title('Rates of vaccinations in NSW per SA4')
    ax.axis('off')
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    plt.setp(ax,xticks=[],yticks=[])
    
    ax_sub = il.zoomed_inset_axes(ax,7,4)
    ax_sub.set_xlim(150.8, 151.5)
    ax_sub.set_ylim(-34.25, -33.5)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    plt.setp(ax_sub,xticks=[],yticks=[])
    
    c1_patch = mpatches.Patch(color=colours[0], label='Percent of people over 15 fully vaccinated')
    c2_patch = mpatches.Patch(color=colours[1], label='Percent of people over 15 with one dose')
    c3_patch = mpatches.Patch(color=colours[2], label='Percent of people over 15 unvaccinated')
    ax.legend(handles=[c3_patch, c2_patch, c1_patch])
    
    for shape in sf.shapeRecords():
        region = shape.record[1]
        if region in nsw_vac_rates:
            p1 = perc_to_float(nsw_vac_rates[region][1])
            p2 = perc_to_float(nsw_vac_rates[region][0])
            num_parts = len(shape.shape.parts)
        
            if num_parts > 1:
                for i in range(num_parts):
                    start = shape.shape.parts[i]
                    if i < num_parts-1:
                        end = shape.shape.parts[i+1]-1
                    else:
                        end = len(shape.shape.points)
            
                    x_list = []
                    y_list = []
                    for point in shape.shape.points[start:end+1]:
                        x_list.append(point[0])
                        y_list.append(point[1])
                    ax.plot(x_list, y_list, color='k', linewidth=0.1)
                    ax_sub.plot(x_list, y_list, color='k', linewidth=0.1)
                    x_lists, y_lists = split_lists(x_list, y_list, p1, p2)
                    for i in range(3):
                        ax.fill(x_lists[i], y_lists[i], color=colours[i])
                        ax_sub.fill(x_lists[i], y_lists[i], color=colours[i])
            else:
                x_list = []
                y_list = []
                for point in shape.shape.points:
                    x_list.append(point[0])
                    y_list.append(point[1])
    
                ax.plot(x_list, y_list, color='k', linewidth=0.1)
                ax_sub.plot(x_list, y_list, color='k', linewidth=0.1)
                x_lists, y_lists = split_lists(x_list, y_list, p1, p2)
                for i in range(3):
                    ax.fill(x_lists[i], y_lists[i], color=colours[i])
                    ax_sub.fill(x_lists[i], y_lists[i], color=colours[i])
    
    il.mark_inset(ax, ax_sub, loc1=2, loc2=3)
    
    plt.savefig('figure_1', bbox_inches='tight')

def generate_fig_2():
    colours = ['#8dd3c7',
               '#ffffb3',
               '#bebada',
               '#fb8072',
               '#80b1d3',
               '#fdb462',
               '#b3de69',
               '#fccde5',
               '#d9d9d9',
               '#bc80bd',
               '#ccebc5',
               '#ffed6f']

    csvf = open('covidData/total_cases_by_age_group.csv', 'r')

    cf = csv.reader(csvf)

    cases_by_age_group = {}

    for i, line in enumerate(cf):
        if i > 0:
            cases_by_age_group[line[0]] = int(line[1])

    plt.clf()
    fig, ax = plt.subplots(figsize=(15,10))

    ax.set_title('Total covid-19 cases per age group \nbetween 29/06/2021 and 31/08/2021')
    ax.bar(cases_by_age_group.keys(), cases_by_age_group.values(), color=colours, edgecolor='k', linewidth=0.5)
    ax.set_xlabel('Age group')
    ax.set_ylabel('Cases')
    ax.set_xticklabels(cases_by_age_group, rotation=45)
    ax.grid(linestyle='--', linewidth=0.5, axis='y', alpha=0.8)
    ax.set_ylim(0, 7000)

    fig.tight_layout()

    # plt.show()
    plt.savefig('figure_2', bbox_inches='tight')

def generate_fig_3():
    sf = shapefile.Reader('SA4_2021_AUST_SHP_GDA2020/SA4_2021_AUST_GDA2020')
    csvf = open('covidData/vaccinations_by_sa4.csv', 'r')

    cf = csv.reader(csvf)

    nsw_vac_rates_no_dose = {}
    nsw_vac_rates_one_dose = {}
    nsw_vac_rates_two_dose = {}

    for line in cf:
        if line[0] == 'NSW':
            nsw_vac_rates_no_dose[line[1]] = perc_to_float('100.00%')
            nsw_vac_rates_one_dose[line[1]] = perc_to_float(line[3])
            nsw_vac_rates_two_dose[line[1]] = perc_to_float(line[2])

    colours = {0:'#756bb1',
               1:'#bcbddc',
               2:'#efedf5'}

    plt.clf()
    fig, ax = plt.subplots(figsize=(15,10))

    ax.set_title('Rates of vaccinations in NSW')
    ax.bar(range(len(nsw_vac_rates_no_dose.keys())), nsw_vac_rates_no_dose.values(), color=colours[2], zorder=0)
    ax.bar(range(len(nsw_vac_rates_two_dose.keys())), nsw_vac_rates_two_dose.values(), color=colours[1], zorder=1)
    ax.bar(range(len(nsw_vac_rates_one_dose.keys())), nsw_vac_rates_one_dose.values(), color=colours[0], zorder=2)
    ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
    ax.set_xticks([])
    for i, area in enumerate(nsw_vac_rates_no_dose.keys()):
        ax.text(-0.15+i, 0.02, area, rotation=90, alpha=0.9)
    c1_patch = mpatches.Patch(color=colours[0], label='People over 15 fully vaccinated')
    c2_patch = mpatches.Patch(color=colours[1], label='People over 15 with one dose')
    c3_patch = mpatches.Patch(color=colours[2], label='People over 15 unvaccinated')
    ax.legend(handles=[c3_patch, c2_patch, c1_patch])

    # plt.show()
    plt.savefig('figure_3', bbox_inches='tight')

def generate_fig_4():
    colours = ['#8dd3c7',
               '#ffffb3',
               '#bebada',
               '#fb8072',
               '#80b1d3',
               '#fdb462',
               '#b3de69',
               '#fccde5',
               '#d9d9d9',
               '#bc80bd',
               '#ccebc5',
               '#ffed6f']

    csvf = open('covidData/total_cases_by_age_group.csv', 'r')

    cf = csv.reader(csvf)

    cases_by_age_group = {}

    for i, line in enumerate(cf):
        if i > 0:
            cases_by_age_group[line[0]] = int(line[1])

    plt.clf()
    patches, texts = plt.pie(cases_by_age_group.values(), colors=colours, startangle=90, wedgeprops={'linewidth':'0.2','edgecolor':'k'})

    plt.legend(patches, cases_by_age_group.keys(), bbox_to_anchor=(0.95,0.95), loc=2)
    plt.title('Total covid-19 cases per age group \nbetween 29/06/2021 and 31/08/2021')
    plt.gca().axis('equal')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)

    # plt.show()
    plt.savefig('figure_4', bbox_inches='tight')

if __name__=="__main__":
    generate_fig_1()
    generate_fig_2()
    generate_fig_3()
    generate_fig_4()