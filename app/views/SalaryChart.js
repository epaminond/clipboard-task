import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

class SalaryChart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      records: [],
    };
  }

  componentDidMount() {
    fetch('/api/records')
      .then(res => res.json())
      .then(jsonRes => this.setState({ records: jsonRes.records }));
  }

  barChartData() {
    const countRecords = filterfunction => this.state.records.filter(filterfunction).length;
    return [
      { name: '>20', records: countRecords(record => record.salary < 20) },
      { name: '20-30', records: countRecords(record => record.salary >= 20 && record.salary < 30) },
      { name: '30-40', records: countRecords(record => record.salary >= 30 && record.salary < 40) },
      { name: '40-50', records: countRecords(record => record.salary >= 40 && record.salary < 50) },
      { name: '>50', records: countRecords(record => record.salary >= 50) },
    ];
  }

  render() {
    return (
      <div>
        {(this.state.records.length === 0) ? (
          'Loading...'
        ) : (
          <BarChart
            width={600}
            height={300}
            data={this.barChartData()}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <XAxis dataKey="name" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Bar dataKey="records" fill="#82ca9d" />
          </BarChart>
        )}
      </div>
    );
  }
}

export default SalaryChart;
