import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth/auth.service';
import { foundToken, showError } from 'src/app/shared/shared';


@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})
export class AuthenticationComponent implements OnInit {
  titleLogin: string = "Login Administration";
  credential = {
    email: "",
    password: "",
  };
  securityObject!: any;
  errors!: string[];

  constructor(private auth: AuthService, private router: Router) {
    this.securityObject = foundToken(this.securityObject)
  }

  ngOnInit(): void {
  }

  loginAdmin() {
    this.auth.login(this.credential).subscribe(res => {
      if (res['token']) {
        console.log("the credential are", res['token'])
        this.router.navigate(['profiles/list'])
        // console.log("the response is", res)
      }
    },
      (error => {
        this.errors = []
        this.errors = error.error
        // console.log("the error is", error.error)
        showError(error, error.status, this.errors, error.error)
      })
    )
  }

}
