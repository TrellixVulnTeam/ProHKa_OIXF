import { Component, OnInit } from '@angular/core';
import { ProfileService } from 'src/app/services/profile/profile.service';
import { showError, toastShow } from 'src/app/shared/shared';
import Swal from 'sweetalert2'

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profiles!: any;
  ownerCLient: string = '';
  users!: any;
  errors!: string[];
  url: string = 'http://127.0.0.1:8000';

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.getProfile()
    this.getClientUsers()
  }

  // ******************************* fetch all profiles and userCLient **************************
  getProfile() {
    this.profileService.getProfile().subscribe(res => {
      this.profiles = res
    })
  }

  getClientUsers() {
    this.profileService.getClientUser().subscribe(res => {
      this.users = res
    })
  }

  // *************************** AFFECT A PROFILE TO A USER CLIENT **********************************
  ownerProfile(event, id: number) {
    // this.profiles = this.profiles.filter((obj: any) => obj !== item)
    var index = this.profiles.findIndex(
      (profile) => profile.id == id);


    return this.profileService.setOwner(id, event['id']).subscribe(res => {
      if (res) {
        if (index !== -1) {
          this.profiles[index] = res
        }
        toastShow('success', "profil mis à jour")
      }
    },
      (error => {
        this.errors = []
        this.errors = error.error
        showError(error, error.status, this.errors, error.error)
      })
    )
  }

  // **************************************** DELETE PROFILE *****************************************
  deleteProfile(item) {
    if (item) {
      Swal.fire({
        title: 'Êtes-vous sûr de vouloir supprimer?',
        // text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui!',
        cancelButtonText: 'Non'
      }).then((result) => {
        if (result.isConfirmed) {
          this.profileService.deleteProfile(item['id']).subscribe(res => {
            this.profiles = this.profiles.filter((obj: any) => obj !== item)
            Swal.fire(
              'Supprimer!',
              item['name'] + " supprimé avec succès",
              'success'
            )
          },
            (error => {
              this.errors = []
              this.errors = error.error
              showError(error, error.status, this.errors, error.error)
            })
          )
        }
      })
    }
  }

}
