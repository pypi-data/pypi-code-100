from .salesforce import get_salesforce_object_records
from ipyaggrid import Grid
import pandas as pd


def show_grid(records):
    df = pd.DataFrame(records)

    css_rules = """
    .value-different {
        color: red;
    }

    """
    cell_class_function = "function(params) { return params.value && params.value.includes('→') ? 'value-different' : ''; }"

    column_defs = [{'field': df.index.name}] + [{'field': c, 'cellClass': cell_class_function} for c in df.columns]
    # print(column_defs)
    column_defs[0]['rowDrag'] = True

    grid_options = {
        'columnDefs': column_defs,
        'defaultColDef': {'sortable': 'true', 'filter': 'true', 'resizable': 'true'},
        'enableRangeSelection': True,
        'rowDragManaged': True,
        'animateRows': True
    }

    grid = Grid(grid_data=df,
                css_rules=css_rules,
                grid_options=grid_options,
                quick_filter=True,
                show_toggle_edit=True,
                export_mode="buttons",
                export_csv=True,
                export_excel=True,
                theme='ag-theme-balham',
                show_toggle_delete=True,
                columns_fit='auto',
                index=False,
                keep_multiindex=False)

    return grid, df, records


def show_salesforce_object(sf, object_name, addition_query_str=None):
    records = get_salesforce_object_records(sf, object_name, addition_query_str)
    return show_grid(records)
