
class Charts {
    constructor() {
        this.colors = ['#1f1847', '#4941ED', '#306DF9', '#EDB141', '#A030F9', '#C8A11C', '#C85B1C','#eb73bb']
        this.negative_colors = ['#F7B294', '#ED6041', '#B06451']
        this.disabled_color = ['#DCE6EC']
    }

    order_status_colors_and_labels(labels) {
        const doc_status_colors = ["#D5B8E6","#F2BDED","#F2BDED","#F2BDED","#F2BDED","#F2BDED","#F2BDED","#D4C2F2","#E8D7F8","#e6e4fb","#fde8bd","#A0F2EA","#D5B8E6","#ffe7e0","#f8e1d8","#f8e1d8","#D5B8E6","#dcfcd4","#dbe6fb","#f8e1d8","#dcfcd4","#dcfcd4","#dbe6fb","#E8D7F8","#E8D7F8","#E8D7F8","#E8D7F8","#E8EDC7","#efdcf5","#d9f9ff","#d9f9ff","#dcfce7","#dcfce7","#C2C8ED","#F0E1C9","#DEFCEA","#E1D5F2","#E8F0D5","#f7efdc","#f0dec7","#e0d8ed","#e0d8ed","#dbe6fb","#f8e1d8","#f8e1d8","#C7D6ED","#C7D6ED","#EEDFF2","#F5E2D3","#f8e1d8","#f8e1d8","#A0F2EA","#A0F2EA","#E8D7F8","#D5B8E6","#D5B8E6","#D5B8E6","#D5B8E6","#D5B8E6","#dcfcd4","#dbe6fb","#D6EDff","#D6EDff","#D6EDff","#A0F2EA","#A0F2EA","#A0F2EA","#D5B8E6","#D5B8E6","#fef08a","#5eead4","#f0abfc","#a5b4fc","#fca5a5","#D5B8E6","#60a5fa","#4ade80","#f43f5e","#e879f9","#818cf8","#ef4444","#ef4444","#2e1065","#2e1065","#2e1065"];
        const doc_status_names = ["Idle","Running","Exited","Disabled","Initialized","Locked","Draft","Active","Cancelled","Submitted","Overdue","Pending Approval","Approved","Rejected","Unpaid","Pending Delivery","Delivered","Partially Paid","Paid","Unreceipted","Partially Receipted","Partially Paid | Pending GRN","Receipted","Pending GRN","Outstanding | Pending GRN","Outstanding","Payed | Pending GRN","Returned","Completed","Pending","Unsettled","Accepted","Ordered","Debited","Credited","Purchased","Sold","Depleted","Depleting","Unclosed","Closed","Stock Transferred","Transfer In","Disposed","Escalated To Disciplinary","Importation Successful","Resolved","Partially Imported","Importation Failed","Open","Expired","Used","In Progress","On Leave","Resigned","Left","Suspended","Terminated","Unretired","Partially Retired","Retired","Pending Review","Resignation Accepted","RFQ Raised","Raised RFQ","Raised RFP","PO Submitted","Pending Importation","Reconciled Reduction","Scheduled","Prospect","Qualification","Needs Analysis","Proposal","Negotiation","Closing","Won","Lost","Follow-up","Renewal","Inactive","Purchase Order Raised","Converted","Responded","Finalize In Case Outcome | Resolved"];
    
        let colors = [];
    
        labels.forEach(label => {
            let index = doc_status_names.indexOf(label);
            if (index !== -1) {
                colors.push(doc_status_colors[index]);
            } else {
                colors.push('#DCE6EC');
            }
        });
    
        return colors;
    }

    static get_element(el) {
        return document.querySelector(`#${el}`) || false
    }

    grouped_bar_chart(element_id, labels = Array, series = Array, config = {
        title: '',
        y_axis_title: '',
        formatter: '',
        width: '100%',
        height: '100%',
        column_width: '50%',
        colors: this.colors,
        show_legend: true,
        legend_position: 'bottom' 
    }) {
        const options = {
            chart: {
                type: 'bar',
                height: config?.height || '100%',
                width: config?.width || '100%',
            },
            plotOptions: {
                bar: {
                    columnWidth: config?.column_width || '50%',
                    horizontal: false,
                    dataLabels: {
                        position: 'top'
                    }
                }
            },
            dataLabels: {
                enabled: false
            },
            series: series || [],
            // Expected Series
            // series: [{
            //     name: 'Series 1',
            //     data: [44, 55, 41, 67, 22, 43]
            //   }, {
            //     name: 'Series 2',
            //     data: [13, 23, 20, 8, 13, 27]
            //   }],
            xaxis: {
                categories: labels,
            },
            yaxis: {
                title: {
                    text: config?.y_axis_title || '',
                    rotate: -90,
                    offsetX: 0,
                    offsetY: 0,
                    style: {
                        color: undefined,
                        fontSize: '12px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 600,
                        cssClass: 'apexcharts-yaxis-title',
                    },
                },
            },
            legend: {
                show: config?.show_legend,
                position: config?.legend_position || 'bottom'
            },
            title: {
                text: config?.title
            },
            colors: config?.colors || [this.colors],
            tooltip: {
                y: {
                    title: {
                        formatter: function (val) {
                            return val + ` ${config?.formatter || ''}`
                        }
                    }
                }
            }
        }
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    donut_chart(element_id, labels = [], values = [], config = {
        title: "",
        width: '100%',
        height: '100%',
        colors: this.colors,
        show_legend: true,
        enable_animations: true,
        legend_position: 'right',
        plot_show: false,
    }) {
        const options = {
            labels: labels,
            series: values,
            chart: {
                animations: {
                    enabled: config?.enable_animations || true,
                },
                width: config?.width || '100%',
                height: config?.height || '100%',
                type: 'donut',
            },
            dataLabels: {
                enabled: false
            },
            fill: { colors: config?.colors || this.colors },
            colors: config?.colors || this.colors,
            legend: {
                show: config?.show_legend,
                position: config?.legend_position || 'right',
            },
            plotOptions: {
                pie: {
                    donut: {
                        labels: {
                            show: config?.plot_show || false,
                            total: {
                                show: true,
                                label: 'Total',
                                formatter: function (w) {
                                  const total = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
                                  return total.toLocaleString(undefined, {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2,
                                  });
                                }
                            }
                        }
                    }
                }
            }
        };
    
        const el = Charts.get_element(element_id);
        el && new ApexCharts(el, options).render();
    }
    

    semi_donut_chart(element_id, labels = Array, values = Array, config = {
        title: '',
        width: '100%',
        height: 160,
        colors: this.colors,
        legend_position: 'right',
        start_angle: -90,
        end_angle: 90,
        offset_y: 10
    }) {
        const options = {
            labels: labels || [],
            series: values || [],
            chart: {
                width: config?.width || '100%',
                type: 'donut',
            },
            plotOptions: {
                pie: {
                    startAngle: config?.start_angle || -90,
                    endAngle: config?.end_angle || 90,
                    offsetY: config?.offset_y || 10
                }
            },

            dataLabels: {
                enabled: false
            },
            fill: { colors: config?.colors || this.colors },
            colors: config?.colors || this.colors,
            legend: {
                position: config?.legend_position || 'right',
                offsetY: 0,
                height: config?.height || 160,
            }
        }
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    column_chart(element_id, labels, series, config = {
        title: '',
        y_axis_title: '',
        formatter: '',
        formatter_decimals: 0,
        width: 300,
        height: 350,
        column_width: '50%',
        show_legend: false,
        positive_color: this.colors[0],
        negative_color: this.negative_colors[0],
        legend_position: 'bottom'
    }) {
        var options = {
            series: Array.isArray(series) ? series : [series], // Ensure series is an array
            chart: {
                type: 'bar',
                height: config?.height || 350
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: config?.column_width || '55%',
                    endingShape: 'rounded'
                },
            },
            legend: {
                show: config?.show_legend,
                position: config?.legend_position || 'bottom',
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            xaxis: {
                categories: labels,
            },
            fill: {
                opacity: 1
            },
            tooltip: {}
        };
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }    
    

    column_chart_with_data_labels(element_id, labels, values, config = {
        title: '',
        y_axis_title: '',
        formatter: '',
        formatter_decimals: 0,
        width: 300,
        height: 350,
        column_width: '50%',
        colors: this.colors,
        legend_position: 'right'
    }) {
        var options = {
            series: [{
                name: 'Age',
                data: values
            }],
            chart: {
                height: 270,
                type: 'bar',
                color: '#f00'
            },
            plotOptions: {
                bar: {
                    borderRadius: 5,
                    dataLabels: {
                        position: 'top',
                    },
                    // colors: '#f00982',
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val + "dys";
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ["#304758"]
                }
            },

            xaxis: {
                categories: labels,
                position: 'bottom',
                axisBorder: {
                    show: true
                },
                axisTicks: {
                    show: true
                },
                tooltip: {
                    enabled: true,
                }
            },
            yaxis: {
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false,
                },
                labels: {
                    show: false,
                    formatter: function (val) {
                        return val + "%";
                    }
                }

            },
        };

        var chart = new ApexCharts(document.querySelector("#olderst-Stock"), options);
        chart.render();
    }

    column_chart_with_negatives(element_id, labels, values, config = {
        title: '',
        y_axis_title: '',
        formatter: null,
        x_formatter:null,
        formatter_decimals: 0,
        width: 300,
        height: 350,
        column_width: '50%',
        positive_color: this.colors[0],
        negative_color: this.negative_colors[0],
        legend_position: 'right',
        x_axis_style: null,
        y_axis_style: null,
        show_y_labels:true,
        show_x_labels:true
    }) {
        const options = {
            series: [{
                name: config?.title || '',
                data: values || []
            }],
            chart: {
                type: 'bar',
                height: config?.height || 350
            },
            plotOptions: {
                bar: {
                    colors: {
                        ranges: [
                            {
                                from: -Infinity,
                                to: 0,
                                color: config?.negative_color || this.negative_colors[0]
                            },
                            {
                                from: 0,
                                to: Infinity,
                                color: config?.positive_color || this.colors[0]
                            }
                        ]
                    },
                    columnWidth: config?.column_width || '60%',
                }
            },
            dataLabels: {
                enabled: false,
            },
            yaxis: {
                title: { text: config?.y_axis_title || '' },
                labels: {
                    show: config?.show_y_labels != undefined ? config?.show_y_labels : true,
                    formatter: function (y) {
                        return config?.formatter ? config?.formatter(y) : y;
                    },
                    style: config?.x_axis_style || {} 
                }
            },
            xaxis: { 
                categories: labels || [] ,
                labels: {
                    show: config?.show_x_labels != undefined ? config?.show_xlabels : true,
                    style: config?.x_axis_style || {},
                    formatter: function (y) {
                        return config?.x_formatter ? config?.x_formatter(y) : y;
                    },
                }
            }
        }
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    line_chart(element_id, labels, values, config = {
        title: '',
        series_title: '',
        formatter_decimals: 0,
        width: 300,
        height: 180,
        line_color: this.colors[0],
        title_align: 'left',
        curve: 'straight' | 'smooth',
        stroke_size: 5,
        enable_markers: false,
        formatter: null,
        x_axis_style:null,
        y_axis_style:null
    }) {
        var options = {
            series: [{
                name: config?.series_title || '',
                data: values || []
            }],
            chart: {
                height: config?.height || 180,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: config?.stroke_size || 5,
                curve: config?.curve || 'straight',
                colors: config?.line_color || this.colors[0]
            },
            markers: {
                size: config?.enable_markers ? (config?.markers_size || 4) : 0,
                colors: config?.markers_color || this.colors[0]
            },
            title: {
                text: config?.title || '',
                align: config?.title_align || 'left'
            },
            grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'],
                    opacity: 0.3
                },
            },
            xaxis: {
                categories: labels || [],
                labels: { style: config?.x_axis_style || {} }
            },
            yaxis: {
                labels: {
                    formatter: config?.formatter || function(val) { return val; },
                    labels: { style: config?.y_axis_style || {} }
                },
            }
        };
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    multi_line_chart(element_id, labels, values, config = {
        title: '',
        y_axis_title: '',
        series_title: '',
        formatter: '',
        width: 300,
        height: 180,
        colors: this.colors,
        title_align: 'left',
        curve: 'straight' | 'smooth',
        stroke_size: 5,
        show_legend:true,
        enable_markers: true,
        markers_color: this.colors[0],
        dash_array: 0,
        formatter: null,
        x_axis_style:null,
        y_axis_style:null
    }) {
        var options = {
            series: values,
            chart: {
                height: config?.height || 400,
                type: 'line',
                zoom: {
                    enabled: false
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: config?.stroke_size || 5,
                curve: config?.curve || 'smooth',
                dashArray: config?.dash_array || 0,
                colors: config?.colors || this.colors
            },
            colors: config?.colors || this.colors,
            title: {
                text: config?.title || '',
                align: config?.title_align || 'left'
            },
            markers: {
                size: config?.enable_markers ? (config?.markers_size || 4) : 0,
                hover: {
                    sizeOffset: 6
                }
            },
            xaxis: {
                categories: labels,
                labels: { style: config?.x_axis_style || {} }
            },
            yaxis: {
                title: {
                    text: config?.y_axis_title || '',
                    rotate: -90,
                    offsetX: 0,
                    offsetY: 0,
                    style: {
                        color: undefined,
                        fontSize: '12px',
                        fontFamily: 'Helvetica, Arial, sans-serif',
                        fontWeight: 600,
                        cssClass: 'apexcharts-yaxis-title',
                    },
                },
                labels: {
                    formatter: config?.formatter || function(val) { return val; },
                    labels: { style: config?.y_axis_style || {} }
                },
            },
            tooltip: {
                // y: {
                //     title: {
                //         formatter: config?.formatter || function(val) { return val; },
                //     }
                // }
            },
            grid: {
                borderColor: '#f1f1f1',
            },
            legend: {
                show: config?.show_legend,
                position: config?.legend_position || 'right',
            }
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    step_line_chart(element_id, labels, values, config = {
        title: '',
        width: 300,
        height: 180,
        colors: this.colors[0],
        title_align: 'left',
        stroke_size: 5,
        enable_markers: true,
        markers_color: this.colors[0]
    }) {
        var options = {
            series: [{
                data: values
            }],
            chart: {
                type: 'line',
                height: config?.height || 300
            },
            stroke: {
                curve: 'stepline',
                width: config?.stroke_size || 5,
                colors: config?.colors || this.colors[0]
            },
            dataLabels: {
                enabled: false
            },
            title: {
                text: config?.title,
                align: config?.title_align || 'left'
            },
            markers: {
                size: config?.enable_markers ? (config?.markers_size || 4) : 0,
                colors: config?.markers_color || this.colors[0],
                hover: {
                    sizeOffset: 4
                }
            }
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    gantt_chart(element_id, labels, values, dependencies, config = {
        title: '',
        y_axis_title: '',
        formatter: '',
        formatter_decimals: 0,
        width: '100%',
        height: '100%',
        column_width: '50%',
        show_legend: true,
        legend_position: 'bottom',
        colors: this.colors,
      }) {
        const el = document.getElementById(element_id);
        if (!el) {
          console.error(`Element with ID ${element_id} not found.`);
          return;
        }
      
        const options = {
          series: [{
            data: values.map((val, index) => ({
              x: labels[index],
              y: {
                start: new Date().getTime(), // adjust start date
                end: new Date().getTime() + val * 24 * 60 * 60 * 1000, // adjust end date
              },
            })),
          }],
          chart: {
            type: 'rangeBar',
            height: config.height,
            width: config.width,
          },
          plotOptions: {
            bar: {
              horizontal: true,
              barHeight: '50%',
            },
          },
          dataLabels: {
            enabled: true,
          },
          xaxis: {
            type: 'datetime',
          },
          yaxis: {
            title: {
              text: config.y_axis_title,
            },
          },
          legend: {
            show: config.show_legend,
            position: config.legend_position,
          },
          title: {
            text: config.title,
          },
          colors: config.colors,
          annotations: {
            points: dependencies.map((dep) => ({
              x: labels.indexOf(dep.to),
              y: labels.indexOf(dep.from),
              label: {
                text: '⇒',
                style: {
                  fontSize: '16px',
                  color: '#333',
                },
              },
            })),
            lines: dependencies.map((dep) => ({
              x1: labels.indexOf(dep.from),
              y1: labels.indexOf(dep.from),
              x2: labels.indexOf(dep.to),
              y2: labels.indexOf(dep.to),
              strokeDashArray: 2,
              lineWidth: 1,
              color: '#333',
            })),
          },
        };
      
        new ApexCharts(el, options).render();
      }

    pie_chart(element_id, labels, values, config = {
        title: '',
        width: 290,
        height: 180,
        colors: this.colors,
        title_align: 'left',
        show_legend: true,
        legend_position: 'bottom'
    }) {
        var options = {
            series: values,
            chart: {
                height: config?.height || 180,
                width: config?.width || 290,
                type: 'pie',
            },
            labels: labels,
            colors: config?.colors || this.colors,
            dataLabels: {
                enabled: false
            },
            legend: {
                show: config?.show_legend || true,
                position: config?.legend_position || 'bottom'
            }
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    monochrome_pie_chart(element_id, labels, values, config = {
        title: '',
        width: 300,
        height: 180,
        colors: this.colors,
        title_align: 'left',
        stroke_size: 5,
        enable_markers: true,
        markers_color: this.colors
    }) {
        var options = {
            series: values,
            chart: {
                width: config?.width || '100%',
                type: 'pie',
            },
            labels: labels,
            theme: {
                monochrome: {
                    enabled: true
                }
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        offset: -5
                    }
                }
            },
            title: {
                text: config?.title
            },
            dataLabels: {
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex]
                    return [name, val.toFixed(1) + '%']
                }
            },
            legend: {
                show: true
            }
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    polar_area_chart(element_id, labels, values, config = {
        title: '',
        width: '100%',
        height: 180,
        colors: this.colors,
        title_align: 'left',
        opacity: 1,
    }) {
        var options = {
            series: values,
            chart: {
                width: config?.width || '100%',
                height: config?.height || '100%',
                type: 'polarArea',
            },
            labels: labels,
            stroke: {
                colors: config?.colors || this.colors
            },
            colors: config?.colors || this.colors,
            fill: {
                opacity: config?.opacity || 0.8
            },
            legend: {
                show: false,
                position: 'bottom'
            }
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    radial_chart(element_id, labels, values, config = {
        title: '',
        width: '100%',
        height: '100%',
        colors: this.colors,
        title_align: 'left',
        size: '70%'
    }) {
        var options = {
            series: values,
            chart: {
                height: config?.height || '100%',
                type: 'radialBar',
            },
            plotOptions: {
                radialBar: {
                    hollow: {
                        size: config?.size || '70%',
                    },
                    track: {
                        strokeWidth: '50%'
                    },
                    dataLabels: {
                        name: {
                            fontSize: '10px',
                        },
                        value: {
                            fontSize: '14px',
                        },
                    }
                },
            },
            labels: labels,
            colors: config?.colors || this.colors
        };

        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    gradient_radial_chart(element_id){
        var options = {
            series: [75],
            chart: {
            height: "100%",
            type: 'radialBar',
            toolbar: {
              show: true
            }
          },
          plotOptions: {
            radialBar: {
              startAngle: -135,
              endAngle: 225,
               hollow: {
                margin: 0,
                size: '70%',
                background: '#fff',
                image: undefined,
                imageOffsetX: 0,
                imageOffsetY: 0,
                position: 'front',
                dropShadow: {
                  enabled: true,
                  top: 3,
                  left: 0,
                  blur: 4,
                  opacity: 0.3
                }
              },
              track: {
                background: '#fff',
                strokeWidth: '67%',
                margin: 0,
                dropShadow: {
                  enabled: true,
                  top: -3,
                  left: 0,
                  blur: 4,
                  opacity: 0.3
                }
              },
          
              dataLabels: {
                show: true,
                name: {
                  offsetY: -10,
                  show: true,
                  color: '#888',
                  fontSize: '17px'
                },
                value: {
                  formatter: function(val) {
                    return `${parseInt(val)}%`;
                  },
                  color: '#111',
                  fontSize: '13px',
                  show: true,
                }
              }
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'dark',
              type: 'horizontal',
              shadeIntensity: 0.4,
              gradientToColors: ['#180e73'],
              inverseColors: true,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100]
            }
          },
          stroke: {
            lineCap: 'round'
          },
          labels: ['Percent'],
          };
  
          var chart = new ApexCharts(Charts.get_element(element_id), options);
          chart.render();
    }

    spark_chart(element_id, labels, values, config = {
        title: '',
        text: '',
        figure: '',
        width: '100%',
        height: '100%',
        colors: this.disabled_color,
        title_align: 'left',
        opacity: 0.4,
        curve: 'straight',
        font_size: '24px',
        tootip_title:""
    }) {
        var options = {
            series: [{
                title: '',
                data: values
            }],
            chart: {
                type: 'area',
                height: config?.height || '100%',
                sparkline: {
                    enabled: true
                },
            },
            labels: labels,
            dataLabels: {
                enabled: true
            },
            stroke: {
                width: 1,
                curve: config?.curve || 'straight'
            },
            fill: {
                opacity: config?.opacity || 0.4,
            },
            yaxis: {
                min: 0
            },
            colors: config?.colors || this.disabled_color,
            title: {
                text: config?.figure || '',
                offsetX: 0,
                style: {
                    fontSize: config?.font_size || '24px',
                }
            },
            subtitle: {
                text: config?.text,
                offsetX: 0,
                style: {
                    fontSize: '11px',
                    color: 'gray',
                    marginTop: '10px'
                }
            },
            tooltip: {
                y: {
                    formatter: (value)=>lite.utils.thousand_separator(value,lite.system_settings?.currency_decimals),
                    title: {
                        formatter: (seriesName) => `<strong>${config?.tootip_title}</strong>` || "",
                    },
                },
            }
        };
        const el = Charts.get_element(element_id)
        el && new ApexCharts(el, options).render() || ''
    }

    stacked_bar_chart(element_id, labels, series, config = {
        column_width: '50%',
    }) {
        const options = {
            chart: {
                type: 'bar',
                height: config.height || '100%',
                width: config.width || '100%',
                stacked: true,
                stackType: config.stacked_type || 'normal'
            },
            plotOptions: {
                bar: {
                    columnWidth: config?.column_width || '50%',
                    horizontal: true,
                }
            },
            series: series,
            xaxis: {
                categories: labels,
            },
            yaxis: {
                title: {
                    text: config.y_axis_title || '',
                    style: {
                        fontSize: '12px',
                        fontWeight: 600,
                    },
                },
            },
            legend: {
                show: config.show_legend !== undefined ? config.show_legend : true,
                position: config.legend_position || 'bottom'
            },
            title: {
                text: config.title || ''
            },
            colors: config.colors || this.colors,
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val;
                    }
                }
            }
        };

        const el = Charts.get_element(element_id);
        el && new ApexCharts(el, options).render();
    }

    tree_map_chart(element_id, series, config = {}) {
        const options = {
            chart: {
                type: 'treemap',
                height: config.height || '100%',
                width: config.width || '100%'
            },
            series: series,
            title: {
                text: config.title || ''
            },
            colors: config.colors || this.colors
        };

        const el = Charts.get_element(element_id);
        el && new ApexCharts(el, options).render();
    }

    stacked_column_chart(element_id, labels, series, config = {
        enable_data_lable: false,
        column_width: '50%',
    }) {
        const options = {
            chart: {
                type: 'bar',
                height: config.height || '100%',
                width: config.width || '100%',
                stacked: true,
                stackType: config.stacked_type || 'normal'
            },
            dataLabels: {
                enabled: config?.enable_data_lable || false,
            },
            plotOptions: {
                bar: {
                    columnWidth: config?.column_width || '50%',
                    horizontal: false,
                }
            },
            series: series,
            xaxis: {
                categories: labels,
            },
            yaxis: {
                title: {
                    text: config.y_axis_title || '',
                    style: {
                        fontSize: '12px',
                        fontWeight: 600,
                    },
                },
            },
            legend: {
                show: config.show_legend !== undefined ? config.show_legend : true,
                position: config.legend_position || 'bottom'
            },
            title: {
                text: config.title || ''
            },
            colors: config.colors || this.colors,
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val;
                    }
                }
            }
        };

        const el = Charts.get_element(element_id);
        el && new ApexCharts(el, options).render();
    }

    waterfall_chart(element_id, series, config = {}) {
        const options = {
            chart: {
                type: 'waterfall',
                height: config.height || '100%',
                width: config.width || '100%'
            },
            series: series,
            yaxis: {
                title: {
                    text: config.y_axis_title || '',
                    style: {
                        fontSize: '12px',
                        fontWeight: 600,
                    },
                },
            },
            title: {
                text: config.title || ''
            },
            colors: config.colors || this.colors,
            legend: {
                show: config.show_legend !== undefined ? config.show_legend : true,
                position: config.legend_position || 'bottom'
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val;
                    }
                }
            }
        };

        const el = Charts.get_element(element_id);
        el && new ApexCharts(el, options).render();
    }


    statistical_chart(
        element_id, 
        data,
        colors=[lite.user?.company?.default_theme_color, lite.user?.company?.default_theme_color],
        horizontal=false){
        var options = {
            series: data,
            chart: {
            height: "100%",
            type: 'bar'
          },
          plotOptions: {
            bar: {
              horizontal: horizontal,
            }
          },
          colors: colors,
          dataLabels: {
            formatter: function(val, opt) {
              const goals =
                opt.w.config.series[opt.seriesIndex].data[opt.dataPointIndex]
                  .goals
          
              if (goals && goals.length) {
                return `${val} / ${goals[0].value}`
              }
              return val
            }
          },
          legend: {
            show: false,
            showForSingleSeries: true,
            // customLegendItems: ['Actual', 'Expected'],
            markers: {
              fillColors: colors
            }
          }
          };
  
          var chart = new ApexCharts(Charts.get_element(element_id), options);
          chart.render();
    }

     
    pattern_chart(
        element_id,
        data,
        colors=[lite.user?.company?.default_theme_color, lite.user?.company?.default_theme_color],
        horizontal=false
    ){
        var options = {
            series: data,
            chart: {
            type: 'bar',
            height: "100%",
            stacked: true,
            dropShadow: {
              enabled: true,
              blur: 1,
              opacity: 0.9
            }
          },
          plotOptions: {
            bar: {
              horizontal: false,
              barHeight: '100%',
            },
          },
          colors: colors,
          dataLabels: {
            enabled: false
          },
          stroke: {
            width: 2,
          },
        //   title: {
        //     text: 'Compare Sales Strategy'
        //   },
        legend: {
            show: false
          },
          xaxis: {
            categories: ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep","Oct","Nov","Dec"],
          },
          yaxis: {
            title: {
              text: undefined
            },
          },
          tooltip: {
            shared: false,
            y: {
              formatter: function (val) {
                return val + "K"
              }
            }
          },
          fill: {
            type: 'pattern',
            opacity: 1,
            pattern: {
              style: ['circles', 'slantedLines', 'verticalLines', 'horizontalLines'],
          
            }
          },
          states: {
            hover: {
              filter: 'none'
            }
          }
          };
  
          var chart = new ApexCharts(Charts.get_element(element_id), options);
          chart.render();
    }

}

export default Charts