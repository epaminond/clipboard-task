import React from 'react';

import Main from '../layouts/Main';
import SalaryChart from './SalaryChart';

const Index = () => (
  <Main>
    <div className="col-sm-12" id="index">
      <h1> Salary Stats </h1>
      <SalaryChart />
    </div>
  </Main>
);

export default Index;
