import { Component, OnInit } from '@angular/core';
import { AlertController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.scss'],
  standalone: false
})
export class ProfilePage implements OnInit {
  // User profile data
  userName: string = 'Kiran Patel';
  userEmail: string = 'kiran.patel.@ftr.com';
  userPhone: string = '+1 (555) 123-4567';
  customerUSI: string = '202401234';

  constructor(
    private alertController: AlertController,
    private toastController: ToastController
  ) { }

  ngOnInit() {
  }

  async editProfile() {
    const alert = await this.alertController.create({
      header: 'Edit Profile',
      inputs: [
        {
          name: 'name',
          type: 'text',
          placeholder: 'Full Name',
          value: this.userName
        },
        {
          name: 'email',
          type: 'email',
          placeholder: 'Email',
          value: this.userEmail
        },
        {
          name: 'phone',
          type: 'tel',
          placeholder: 'Phone Number',
          value: this.userPhone
        },
        {
          name: 'customerUSI',
          type: 'text',
          placeholder: 'Customer USI',
          value: this.customerUSI,
          disabled: true
        }
      ],
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel'
        },
        {
          text: 'Save',
          handler: (data) => {
            if (data.name && data.email) {
              this.userName = data.name;
              this.userEmail = data.email;
              this.userPhone = data.phone || this.userPhone;
              // customerUSI is readonly, not updated
              this.showToast('Profile updated successfully!');
              return true;
            } else {
              this.showToast('Name and email are required', 'warning');
              return false;
            }
          }
        }
      ]
    });

    await alert.present();
  }

  async showToast(message: string, color: string = 'success') {
    const toast = await this.toastController.create({
      message: message,
      duration: 2000,
      position: 'bottom',
      color: color
    });
    toast.present();
  }

  async confirmLogout() {
    const alert = await this.alertController.create({
      header: 'Logout',
      message: 'Are you sure you want to logout?',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel'
        },
        {
          text: 'Logout',
          role: 'destructive',
          handler: () => {
            this.logout();
          }
        }
      ]
    });

    await alert.present();
  }

  logout() {
    // Implement logout logic here
    this.showToast('Logged out successfully', 'primary');
    // Navigate to login page or perform logout action
  }
}
