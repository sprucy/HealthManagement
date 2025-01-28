import ReactEChartsCore from 'echarts-for-react/lib/core';
// Import the echarts core module, which provides the necessary interfaces for using echarts.
import * as echarts from 'echarts/core';
// Import charts, all with Chart suffix
import {
  //LineChart,
  //BarChart,
  // PieChart,
  // ScatterChart,
  // RadarChart,
  // MapChart,
  // TreeChart,
  // TreemapChart,
  // GraphChart,
  // GaugeChart,
  // FunnelChart,
  // ParallelChart,
  // SankeyChart,
  // BoxplotChart,
  // CandlestickChart,
  // EffectScatterChart,
  LinesChart,
  // HeatmapChart,
  // PictorialBarChart,
  // ThemeRiverChart,
  // SunburstChart,
  // CustomChart,
} from 'echarts/charts';
// import components, all suffixed with Component
import {
  // GridSimpleComponent,
  GridComponent,
  // PolarComponent,
  // RadarComponent,
  // GeoComponent,
  // SingleAxisComponent,
  // ParallelComponent,
  // CalendarComponent,
  // GraphicComponent,
  // ToolboxComponent,
  TooltipComponent,
  // AxisPointerComponent,
  // BrushComponent,
  TitleComponent,
  // TimelineComponent,
  // MarkPointComponent,
  // MarkLineComponent,
  // MarkAreaComponent,
  LegendComponent,
  // LegendScrollComponent,
  // LegendPlainComponent,
  // DataZoomComponent,
  // DataZoomInsideComponent,
  // DataZoomSliderComponent,
  // VisualMapComponent,
  // VisualMapContinuousComponent,
  // VisualMapPiecewiseComponent,
  // AriaComponent,
  // TransformComponent,
  DatasetComponent,
} from 'echarts/components';
// Import renderer, note that introducing the CanvasRenderer or SVGRenderer is a required step
import {
  CanvasRenderer,
  // SVGRenderer,
} from 'echarts/renderers';
// Register the required components
echarts.use(
    [
        TitleComponent,
        LegendComponent,
        TooltipComponent,
        GridComponent,
        DatasetComponent,
        LinesChart,
        CanvasRenderer,
    ]
);

interface Props {
    title?: string;
    height?: string;
    dataset?: any;
}

const HealthAreaChart = ({ title, height, dataset }: Props) => {
    const getOption = () => {
        return {
            // 示例配置，根据实际需求调整
            title: {
                text: title,
            },
            legend: {},
            tooltip: {},
            dataset: {source:dataset},
            xAxis: {
                type: 'category' ,
            },
            yAxis: {},
            series: [
                { type: 'line', areaStyle: {} }, 
                { type: 'line', areaStyle: {} }, 
                { type: 'line', areaStyle: {} },
                { type: 'line', areaStyle: {} },                
                { type: 'line', areaStyle: {} },                
            ],
        };
    };
    const onChartReadyCallback = () => {
        // 处理图表准备就绪的逻辑
        console.log('Chart is ready');
    };

    
    const EventsDict = {
        click: (params: any) => {
            console.log('Chart clicked:', params);
        },
        // 其他事件处理函数
    };
    return (
        <ReactEChartsCore
            echarts={echarts}
            option={getOption()}
            notMerge={true}
            lazyUpdate={true}
            theme={"theme_name"}
            onChartReady={onChartReadyCallback}
            onEvents={EventsDict}
            style={{ height: height ? `${height}px` : '300px', width: '100%' }}
        />
    );
};
export default HealthAreaChart;

