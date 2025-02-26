export const ColorLegend = ( 
    legendGroup,
    colorScale, tickSpacing=20, 
    tickSize=10, tickTextOffset=20 
) => {
        colorScale.domain().map((domainValue, i) => {
            const group = legendGroup.append('g')
                .attr('class', 'tick')
                .attr('transform',`translate(0, ${i * tickSpacing})`)
            group.append('circle')
                .attr('fill', colorScale(i))
                .attr('r', tickSize)
            group.append('text')
                .attr('dy', '.32em')
                .attr('x', tickTextOffset)
                .text(domainValue)
        })
    };