import { Component } from '@angular/core';
import { EmployeeService } from '../services/employee.service';

@Component({
  selector: 'app-employee-table',
  standalone: true,
  imports: [],
  templateUrl: './employee-table.component.html',
  styleUrl: './employee-table.component.css'
})
export class EmployeeTableComponent {

  employees = false;
  employeesList = [{
    'code': 1,
    'name': 'Adas',
    'lastname': 'asdas',
    'department': 'eadas',
    'job': 'chambeador',
    'date': '2021-08-98'
  }];

  constructor(private employeeService: EmployeeService) { }

  //Obtener lista de empleados
  getEmployees() {
    /*this.employeeService.getEmployees()
    .subscribe(
      res => {
        let data:any = res;
        if (data.length > 0){
          this.employees = true;
          

          {
    'code': 1,
    'name': 'Adas',
    'lastname': 'asdas',
    'department': 'eadas',
    'job': 'chambeador',
    'date': '2021-08-98'
  }
    
          this.employeesList = data;
        } else{
          this.employeesList = [];
        }
      },
      err => {
        alert(err);
      }
    )*/
   
  }
}
