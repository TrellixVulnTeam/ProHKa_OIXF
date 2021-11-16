import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';
import { NgSelectModule } from '@ng-select/ng-select';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthenticationComponent } from './components/authentication/authentication.component';
import { HeaderComponent } from './components/header/header.component';
import { ProfileComponent } from './components/profile/profile.component';
import { ROUTING } from './app-routing';
import { UrlPipePipe } from './pipe/url-pipe.pipe';
import { AddEditProfileComponent } from './components/profile/add-edit-profile/add-edit-profile.component';
import { DemandeComponent } from './components/demande/demande.component';
import { MessageComponent } from './components/message/message.component';
import { EvaluationComponent } from './components/evaluation/evaluation.component';

@NgModule({
  declarations: [
    AppComponent,
    AuthenticationComponent,
    HeaderComponent,
    ProfileComponent,
    UrlPipePipe,
    AddEditProfileComponent,
    DemandeComponent,
    MessageComponent,
    EvaluationComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgSelectModule,
    ROUTING,
    SweetAlert2Module.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
