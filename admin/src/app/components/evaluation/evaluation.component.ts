import { Component, OnInit } from '@angular/core';
import { ProfileService } from 'src/app/services/profile/profile.service';

@Component({
  selector: 'app-evaluation',
  templateUrl: './evaluation.component.html',
  styleUrls: ['./evaluation.component.css']
})
export class EvaluationComponent implements OnInit {

  notes!: any;
  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.getAllEvaluationCandidate()
  }

  getAllEvaluationCandidate() {
    return this.profileService.getAllNotes().subscribe(res => {
      this.notes = res
    })
  }

}
