from .data_processing import sidebar_and_upload,\
                            apply_filters, \
                            crud_operations,\
                            generate_pandas_profiling,\
                            load_gdf
                            
from .visualization import plot_classification_heatmap,\
                            plot_selected_category, \
                            plot_heatmap, \
                            plot_time_trends, \
                            plot_total_patients,\
                            plot_time_trends_line,\
                            wordcloud_or_hist_box_plot,\
                            plot_bubble_chart,\
                            plot_animated_bubble_chart
                            
from .interactive_maps import folium_static,\
                            generate_interactive_maps,\
                            plot_patients_by_ayuntamiento,\
                            plot_average_metrics_by_ayuntamiento,\
                            plot_top_ayuntamientos_for_category
                            
from .utils import ui_info, ui_spacer

from .data_test import generate_data