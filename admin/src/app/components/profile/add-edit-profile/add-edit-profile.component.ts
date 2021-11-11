import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ProfileService } from 'src/app/services/profile/profile.service';
import { showError, toastShow } from 'src/app/shared/shared';

@Component({
  selector: 'app-add-edit-profile',
  templateUrl: './add-edit-profile.component.html',
  styleUrls: ['./add-edit-profile.component.css']
})
export class AddEditProfileComponent implements OnInit {

  formProfile!: FormGroup;
  errors!: string[];
  imagSrc!: string;
  constructor(private fb: FormBuilder, private profileService: ProfileService,
    private cd: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.formProfile = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(4)]],
      surname: [''],
      email: [''],
      phone: [''],
      dateBorn: [''],
      placeBorn: [''],
      age: [''],
      city: [''],
      language: [''],
      religion: [''],
      situation: [''],
      children: [''],
      mainImg: [null],
      availability: [true],
      fileUpload: this.fb.array([this.uploadFile()])
    })
  }

  private uploadFile(): FormGroup {
    return this.fb.group({
      fileToSend: [''],
    });
  }

  public get fileList(): FormArray {
    return this.formProfile.get('fileUpload') as FormArray;
  }

  public addFile(): void {
    return this.fileList.push(this.uploadFile());
  }

  // ************************* mainImg  and preview ************************************************
  onFileChange(event) {
    const file = (event.target as HTMLInputElement).files[0]
    this.formProfile.patchValue({
      mainImg: file //on affecte a la variable l'image recu
    })
    this.formProfile.get('mainImg').updateValueAndValidity()
    //**** preview *************/ 
    const reader = new FileReader();
    reader.onload = () => {
      this.imagSrc = reader.result as string;
    }
    reader.readAsDataURL(file)
  }

  // ******************************* others images *******************************************
  // listenning event onChange in field img
  public setFileChange(event: Event | any, index: number): void {
    let reader = new FileReader();
    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;
      reader.readAsDataURL(file);
      reader.onload = () => {
        // passons les valeurs dynamiquement
        this.formProfile.get('fileUpload')?.get(`${index}`)?.patchValue({
          fileToSend: { 'name': file.name, 'file': reader.result }
        });
        // let array = this.archiveFrom.get('fileUpload')?.get(`${index}`)?.value
        // console.log("the old path is ", array["titleFile"])
        // if (this.edit && array) {
        //   this.deleteOldFile.push(this.checkPathToDelete[index])
        //   // console.log("the path to add ", this.deleteOldFile)
        //   // console.log("the path before ", this.deleteOldFile)
        // }

        this.cd.markForCheck();

      }
    }
  }


  // *********************************** register profile ******************************************
  registerProfile() {
    this.profileService.registerProfile(this.formProfile.value).subscribe(res => {
      if (res) {
        toastShow("success", "Archive enregistrée avec succès")
        this.errors = []
        this.ngOnInit()
      }
      // console.log("files to send are", res)

    },
      (error => {
        this.errors = []
        this.errors = error.error
        showError(error, error.status, this.errors, error.error)
      })
    )
  }

}
