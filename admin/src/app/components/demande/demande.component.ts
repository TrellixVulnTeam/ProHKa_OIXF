import { Component, OnInit } from '@angular/core';
import { ProfileService } from 'src/app/services/profile/profile.service';
import { showError, toastShow } from 'src/app/shared/shared';
import Swal from 'sweetalert2'

@Component({
  selector: 'app-demande',
  templateUrl: './demande.component.html',
  styleUrls: ['./demande.component.css']
})
export class DemandeComponent implements OnInit {

  commands!: any;
  url: string = "http://127.0.0.1:8000";
  status: string;

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.getCommands();
  }

  getCommands() {
    return this.profileService.getAllCommand().subscribe(res => {
      this.commands = res
    })
  }

  sendStatus(id: number, event) {
    return this.profileService.sendStatus(id, event.target.value).subscribe(res => {
      if (res) {
        toastShow('success', "Statut mis à jour")
      }
    })
  }

  deleteComand(item: []) {
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
          this.profileService.deleteCommand(item['id']).subscribe(res => {
            this.commands = this.commands.filter((obj: any) => obj !== item)
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

}
