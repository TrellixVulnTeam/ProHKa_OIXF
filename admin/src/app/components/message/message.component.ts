import { Component, OnInit } from '@angular/core';
import { ProfileService } from 'src/app/services/profile/profile.service';
import { showError, toastShow } from 'src/app/shared/shared';
import Swal from 'sweetalert2'


@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit {

  profiles!: any;
  messages!: any;
  selected!: [];

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.retrieveAllMessage();
    this.getProfile()
  }

  retrieveAllMessage() {
    return this.profileService.getAllMessage().subscribe(res => {
      this.messages = res
    })
  }

  // *************************** change status *****************************************
  sendStatu(id: number, event) {
    return this.profileService.sendStatusMessage(id, event.target.value).subscribe(res => {
      if (res) {
        toastShow('success', "Statut mis à jour")
      }
    })
  }

  deleteMsg(item: []) {
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
          this.profileService.deleteMessage(item['id']).subscribe(res => {
            this.messages = this.messages.filter((obj: any) => obj !== item)
            Swal.fire(
              'Supprimer!',
              item['name'] + " supprimé avec succès",
              'success'
            )
          })
        }
      })
    }
  }

  // ******************************* fetch all profiles **************************
  getProfile() {
    this.profileService.getProfile().subscribe(res => {
      this.profiles = res
    })
  }

  selectProfileToSend(event) {
    this.selected = event
  }

  // *************************** send proposition to client *****************************************
  sendProposition(item: any) {
    let data = { "id": item.id, "profile": this.selected }
    if (item && this.selected) {
      Swal.fire({
        title: `Êtes-vous sûr de vouloir cet email à ${item.name}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui!',
        cancelButtonText: 'Non'
      }).then((result) => {
        if (result.isConfirmed) {
          this.profileService.proposition(data).subscribe(res => {
            if (res) {
              toastShow('success', "Email envoyé avec succès")
              this.ngOnInit()
            }
          })
        }
      })
    }
  }

}
