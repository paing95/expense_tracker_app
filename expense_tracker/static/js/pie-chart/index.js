import { Arcs } from "/static/js/pie-chart/arcs.js";
import { ColorLegend } from "/static/js/pie-chart/colorLegend.js";

export const PieChart = (data, id, width, height, fields, legend) => {
    const xAxisValue = 10;
    const yAxisValue = 200;
    const xLegendValue = 180;
    const yLegendValue = -150;

    const radius = Math.min(width, height) / 2.5;
    const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr("class", "pie-chart");

    const svgGroup = svg.append('g')
        .attr("transform", "translate(" + ((width / 2) - 100) + "," + ((height / 2) - 30) + ")");
    
    const colorScale = d3.scaleOrdinal()
        .domain(fields)
        .range(d3.schemeDark2);
    
    const pie = d3.pie()
        .value(d => d[1]);
    
    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    const legendGroup = svgGroup.append('g')
        .attr('transform', `translate(${xLegendValue}, ${yLegendValue})`)

    ColorLegend(legendGroup, colorScale, 25);
    
    Arcs(data, arc, svgGroup, pie, colorScale, 10);

    svgGroup.append('text')
        .attr('class', 'axis-label')
        .attr('x', xAxisValue)
        .attr('y', yAxisValue)
        .attr('style', 'text-anchor: middle')
        .text(legend);

}