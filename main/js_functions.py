from bokeh.models import CustomJS
def DateRangeSlider_callback(source,filter):
    daterange_callback = CustomJS(args=dict(source=source,filter=filter),
    code="""
        const indices = [];
        for(var i=0;i<source.get_length();i++){
            const current_value = cb_obj.value;
            const current_date = source.data['date'][i];
            if(current_date >= current_value[0]&& current_date<=current_value[1]){
                indices.push(i);
            }
        }
        filter.indices = indices;
        source.change.emit();
    """
    )
    return daterange_callback

def Button_callback(source,filter,select):
    button_callback = CustomJS(args=dict(select=select,source=source,filter=filter),
    code="""
        const indices = [];
        for(var i=0;i<source.get_length();i++){
            const current_value = select.value;
            const current_date = source.data['date'][i];
            if(current_date >= current_value[0]&& current_date<=current_value[1]){
                indices.push(i);
            }
        }
        filter.indices = indices;
        source.change.emit();
    """
    )
    return button_callback

def Dropdown_y1_callback(source,glyph,plot,legend_item,legend_dict):
    dropdown_callback = CustomJS(args=dict(source=source,glyph=glyph,plot=plot,legend_item=legend_item,legend_dict=legend_dict),
    code="""
        var value = this.item;
        glyph.glyph.y.field = value;
        legend_item.label = legend_dict[value];
        plot.y_range.start = Math.min.apply(null,source.data[value]);
        plot.y_range.end = Math.max.apply(null,source.data[value]);
        source.change.emit();
    """
    )
    return dropdown_callback

def Dropdown_y2_callback(source,glyph,plot,legend_item,legend_dict):
    dropdown_callback = CustomJS(args=dict(source=source,glyph=glyph,plot=plot,legend_item=legend_item,legend_dict=legend_dict),
    code="""
        var value = this.item;
        glyph.glyph.y.field = value;
        legend_item.label = legend_dict[value];
        plot.extra_y_ranges.extra_range.start = Math.min.apply(null,source.data[value]);
        plot.extra_y_ranges.extra_range.end = Math.max.apply(null,source.data[value]);
        source.change.emit();
    """
    )
    return dropdown_callback