import React, {useMemo} from 'react';
import {Area, AreaChart, ComposedChart, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import './App.css';
import _ from "lodash";

const taxes:TaxDataFile = require('./tax_df_full.json');

interface DataPoint {
    x: number
    y: number
    deltay?:number
}

interface TaxDataFile {
    schema:any
    data:TaxDataPoint[]
}

interface TaxDataPoint {
    pretax_income:number
    tax:number
    after_tax_income:number
    marginal_after_tax_income_increase:number
    marginal_tax:number
}

function App() {

    function reshape_data(taxes: TaxDataFile) {
        let raw_data = taxes.data;
        raw_data.forEach(value=>{
            value.marginal_tax = _.floor(value.marginal_tax,2)
        })
        return raw_data;

    }

    const data:TaxDataPoint[] = useMemo(() => reshape_data(taxes), [taxes])

    console.log(taxes)

    return (
        <div className="App">

            {data &&


                <ResponsiveContainer minHeight={400}>
                    <ComposedChart data={data}>

                        <Area yAxisId={'total_tax_rate'} dataKey={'total_tax_rate'}/>
                        <Line strokeWidth={2} stroke={'red'} dot={false} yAxisId={'marginal_tax'} dataKey={'marginal_tax'}/>

                        <XAxis type={'number'} dataKey={'pretax_income'}/>
                        <YAxis tickFormatter={v => `${v * 100}%`} type={'number'} yAxisId={'marginal_tax'} dataKey={'marginal_tax'}/>
                        <YAxis orientation={'right'}  tickFormatter={v => `${v * 100}%`} type={'number'} yAxisId={'total_tax_rate'}
                               dataKey={'total_tax_rate'}/>

                        <Tooltip/>
                    </ComposedChart>


                </ResponsiveContainer>
            }


        </div>
    );
}

export default App;
