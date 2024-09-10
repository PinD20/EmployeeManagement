import { Component } from '@angular/core';
import { EmployeeService } from '../services/employee.service';
import { DepartmentService } from '../services/department.service';
import { FormGroup, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-employee-table',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './employee-table.component.html',
  styleUrl: './employee-table.component.css'
})
export class EmployeeTableComponent {

  employeesList: any = []; //Lista de empleados
  departmentsList: any = []; //Lista de departamentos
  createEmployeeForm: FormGroup; //Formulario para crear empleado
  editEmployeeForm: FormGroup; //Formulario para editar empleado

  constructor(
    private employeeService: EmployeeService,
    private departmentService: DepartmentService,
    private formBuilder: FormBuilder
  ) { 
    this.getEmployees();
    this.createEmployeeForm = this.formBuilder.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      codigo_departamento: [0],
      cargo: ['', Validators.required],
      fecha_contratacion: ['', Validators.required]
    });
    this.editEmployeeForm = this.formBuilder.group({
      codigo: [0],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      codigo_departamento: [0],
      cargo: ['', Validators.required],
      fecha_contratacion: ['', Validators.required]
    });
  }

  //Obtener lista de empleados
  getEmployees() {
    this.employeeService.getEmployees()
    .subscribe(
      res => {
        let data:any = res;
        this.employeesList = data.employees;
      },
      err => {
        alert(err);
      }
    )
  }

  //Obtener lista de departamentos
  getDepartments() {
    this.departmentService.getDepartments()
    .subscribe(
      res => {
        let data:any = res;
        this.departmentsList = data.departments;
      },
      err => {
        alert(err);
      }
    )
  }

  deleteEmployee(employee: any){
    Swal.fire({
      title: '¿Estás seguro?',
      text: `Se eliminará al empleado ${employee.nombre} ${employee.apellido}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, continuar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        this.employeeService.deleteEmployee(employee.codigo)
        .subscribe(
          res => {
            //Actualiza la lista de empleados
            this.getEmployees();
            Swal.fire({
              title: "Empleado eliminado",
              text: "El empleado fue eliminado con éxito.",
              icon: "success"
            });
          },
          err => {
            console.log(err);
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "Ocurrió un error durante la eliminación del empleado.",
            });
          }
        )
      }
    });
  }

  openCreateModal(){
    this.getDepartments(); //Obtener lista de departamentos

    //Setear valores en blanco
    this.createEmployeeForm.setValue({
      nombre: '',
      apellido: '',
      codigo_departamento: 0,
      cargo: '',
      fecha_contratacion: (new Date()).toISOString().split('T')[0]
    });

    //Abrir formulario de edición
    const modal = new (window as any).bootstrap.Modal(document.getElementById('createEmployeeModal'));
    modal.show();
  }

  // Crear empleado
  onSubmitCreate() {
    if (this.createEmployeeForm.valid) {
      let newEmployee = this.createEmployeeForm.value;
      newEmployee.codigo_departamento = +newEmployee.codigo_departamento;
      this.employeeService.createEmployee(newEmployee)
      .subscribe(
        res => {
          this.getEmployees(); //Actualizar lista de empleados
          alert("ok")
        },
        err => {
          alert(err);
          console.log(err)
        }
      )

      // Cerrar el modal después de guardar los cambios
      const modal = (window as any).bootstrap.Modal.getInstance(document.getElementById('createEmployeeModal'));
      modal.hide();
    } else {
      alert("Formulario inválido");
    }
  }

  openEditModal(employee: any){
    this.getDepartments(); //Obtener lista de departamentos

    //Setear valores del empleado en el formulario
    this.editEmployeeForm.setValue({
      codigo: employee.codigo,
      nombre: employee.nombre,
      apellido: employee.apellido,
      codigo_departamento: employee.codigo_departamento,
      cargo: employee.cargo,
      fecha_contratacion: employee.fecha_contratacion
    });

    //Abrir formulario de edición
    const modal = new (window as any).bootstrap.Modal(document.getElementById('editEmployeeModal'));
    modal.show();
  }

  // Guardar cambios de edición
  onSubmitEdit() {
    if (this.editEmployeeForm.valid) {
      let editedEmployee = this.editEmployeeForm.value;
      editedEmployee.codigo_departamento = +editedEmployee.codigo_departamento;
      this.employeeService.editEmployee(editedEmployee)
      .subscribe(
        res => {
          this.getEmployees(); //Actualizar lista de empleados
          alert("ok")
        },
        err => {
          alert(err);
          console.log(err)
        }
      )

      // Cerrar el modal después de guardar los cambios
      const modal = (window as any).bootstrap.Modal.getInstance(document.getElementById('editEmployeeModal'));
      modal.hide();
    } else {
      alert("Formulario inválido");
    }
  }
}
