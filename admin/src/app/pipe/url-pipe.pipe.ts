import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Pipe({
  name: 'urlPipe'
})
export class UrlPipePipe implements PipeTransform {

  constructor(private domSanitizer: DomSanitizer) { }
  transform(value: any, prefix = '') {
    return this.domSanitizer.bypassSecurityTrustUrl(prefix + value);
  }

}
