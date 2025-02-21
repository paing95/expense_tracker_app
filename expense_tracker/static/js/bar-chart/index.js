import { AxisBottom } from "/static/js/bar-chart/axisBottom.js";
import { AxisLeft } from "/static/js/bar-chart/axisLeft.js";
import { Marks } from "/static/js/bar-chart/marks.js";

export const BarChart = (data, id, width, height, xField, yField, legend) => {
    const margin = {
        top: 20,
        right: 50,
        bottom: 100, 
        left: 220
    };
    const xAxisOffsetValue = 50;
    const innerHeight = height - margin.top - margin.bottom;
    const innerWidth = width - margin.left - margin.right;

    const xValue = d => d[xField];
    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, xValue) + 100])
        .range([0, innerWidth]);
    const xAxisTickFormat = value => d3.format('$.2f')(value);

    const yValue = d => d[yField];
    const yScale = d3.scaleBand()
        .domain(data.map(yValue))
        .range([0, innerHeight])
        .paddingInner(0.2);

    const svg = d3.select(id).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("class", "bar-chart");

    const svgGroup = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    /* x-Axis */
    AxisBottom(xScale, innerHeight, svgGroup);

    /* y-Axis */
    AxisLeft(yScale, svgGroup);

    svgGroup.append('text')
        .attr('class', 'axis-label')
        .attr('x', innerWidth / 2)
        .attr('y', innerHeight + xAxisOffsetValue)
        .attr('style', 'text-anchor: middle')
        .text(legend);
    
    /* Bars */
    Marks(data, svgGroup, xValue, xScale, yValue, yScale, xAxisTickFormat);

    return svgGroup;
}