import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NgSwitch, NgSwitchCase, NgSwitchDefault } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [
    RouterOutlet, // For routing
    NgSwitch, NgSwitchCase, NgSwitchDefault, // For ngSwitch directives
  ],
})
export class AppComponent {
  title = 'angular-test';
  selection = { value: '' }; // Initialize selection to avoid undefined errors
}