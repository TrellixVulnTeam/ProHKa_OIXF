import { RouterModule, Routes } from "@angular/router";
import { AuthenticationComponent } from "./components/authentication/authentication.component";
import { DemandeComponent } from "./components/demande/demande.component";
import { MessageComponent } from "./components/message/message.component";
import { ProfileComponent } from "./components/profile/profile.component";
// import { SingleArchiveComponent } from "./components/archives/single-archive/single-archive.component";


const appRoutes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', component: AuthenticationComponent },//canActivate:[Auth1Guard]
    { path: 'demande', component: DemandeComponent },//canActivate:[Auth1Guard]
    { path: 'message', component: MessageComponent },//canActivate:[Auth1Guard]
    {
        path: "profiles",
        children: [
            { path: "list", component: ProfileComponent },
        ]
    },
    // {path: "show-archive/:id", component:SingleArchiveComponent} //, canActivate:[AuthGuard], data:{claimName:'role'} , canActivate:[AuthGuard]
]

export const ROUTING = RouterModule.forRoot(appRoutes)