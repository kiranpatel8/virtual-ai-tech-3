import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Camera, CameraResultType, CameraSource, Photo } from '@capacitor/camera';
import { AlertController, LoadingController, ToastController } from '@ionic/angular';
import { firstValueFrom } from 'rxjs';
import { DeviceIdentifierService, DeviceIdentificationResponse, HealthResponse } from '../services/device-identifier.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false
})
export class HomePage implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  
  capturedImage: string | null = null;
  identificationResult: DeviceIdentificationResponse | null = null;
  isLoading = false;
  apiHealthy = false;

  healthStatus: string | null = null;

  health: HealthResponse | null = null;
  
  // Webcam properties
  showWebcam = false;
  webcamStream: MediaStream | null = null;

  constructor(
    private deviceService: DeviceIdentifierService,
    private alertController: AlertController,
    private loadingController: LoadingController,
    private toastController: ToastController
  ) {}

  ngOnInit() {
    this.checkApiHealth();
  }

  /**
   * Check if the Python API is healthy and configured
   */
  async checkApiHealth() {
    try {
          const health = await firstValueFrom(this.deviceService.checkHealth());
          this.healthStatus = health?.status;
          this.apiHealthy = health?.status === 'healthy' && health?.huggingface_configured;

          
          if (!this.apiHealthy) {
            this.showToast('API is not properly configured. Please check the Python service.', 'warning');
          }
    } catch (error) {
      console.error('API health check failed:', error);
      this.apiHealthy = false;
      this.showToast('Cannot connect to Python API. Make sure it\'s running on localhost:8000', 'danger');
    }
  }

  /**
   * Take a photo using the device camera
   */
  async takePicture() {
    try {
      // Try Capacitor camera first (works on mobile devices)
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.Base64,
        source: CameraSource.Camera
      });

      if (image.base64String) {
        this.capturedImage = `data:image/jpeg;base64,${image.base64String}`;
        this.identificationResult = null; // Clear previous results
        
        // Automatically identify the device after taking the photo
        await this.identifyDevice(image);
      }
    } catch (error: any) {
      console.error('Capacitor camera error:', error);
      
      // Fallback to browser webcam if Capacitor camera fails
      if (error.message?.includes('not available') || error.message?.includes('not implemented')) {
        console.log('Falling back to browser webcam...');
        await this.takePictureWithWebcam();
      } else {
        this.showAlert('Camera Error', 'Failed to take picture. Please try again.');
      }
    }
  }

  /**
   * Use browser's webcam API as fallback for laptop/desktop testing
   */
  async takePictureWithWebcam() {
    try {
      // Check if browser supports webcam
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        this.showAlert('Webcam Not Supported', 'Your browser does not support webcam access. Try "Select from Gallery" instead.');
        return;
      }

      console.log('Requesting webcam access...');
      
      // Request webcam access with simpler constraints
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });

      console.log('Webcam access granted!');
      
      // Give user time to see the camera feed (2 seconds)
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Create video element to capture frame
      const video = document.createElement('video');
      video.srcObject = stream;
      video.autoplay = true;
      video.playsInline = true;
      video.muted = true;

      // Wait for video to be ready
      await new Promise<void>((resolve) => {
        video.onloadedmetadata = () => {
          video.play();
          resolve();
        };
      });

      // Wait a bit more for video to start
      await new Promise(resolve => setTimeout(resolve, 500));

      // Create canvas to capture image
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 1280;
      canvas.height = video.videoHeight || 720;
      const context = canvas.getContext('2d');
      
      if (context && canvas.width > 0 && canvas.height > 0) {
        // Draw video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert to base64
        const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
        const base64Image = dataUrl.split(',')[1];
        
        // Stop webcam
        stream.getTracks().forEach(track => track.stop());
        
        console.log('Image captured successfully!');
        
        // Set captured image
        this.capturedImage = dataUrl;
        this.identificationResult = null;
        
        // Create Photo object for identification
        const photo: Photo = {
          base64String: base64Image,
          format: 'jpeg',
          saved: false
        };
        
        // Identify device
        await this.identifyDevice(photo);
      } else {
        stream.getTracks().forEach(track => track.stop());
        this.showAlert('Capture Error', 'Failed to capture image from webcam.');
      }
      
    } catch (error: any) {
      console.error('Webcam error:', error);
      console.error('Error name:', error.name);
      console.error('Error message:', error.message);
      
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        this.showAlert('Permission Denied', 'Please allow camera access to use this feature. Click the camera icon in your browser\'s address bar.');
      } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        this.showAlert('No Camera Found', 'No camera detected. Please connect a camera or use "Select from Gallery".');
      } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
        this.showAlert('Camera In Use', 'Camera is already in use by another application. Please close other apps using the camera.');
      } else {
        this.showAlert('Webcam Error', `Failed to access webcam: ${error.message || 'Unknown error'}. Try "Select from Gallery" instead.`);
      }
    }
  }

  /**
   * Select an image from the gallery using native file input (preserves filename)
   */
  async selectFromGallery() {
    // Trigger the hidden file input
    this.fileInput.nativeElement.click();
  }

  /**
   * Handle file selection from native file input
   */
  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    
    if (!file) {
      return;
    }

    try {
      console.log('Selected file:', file.name, 'Type:', file.type, 'Size:', file.size);

      // Validate file is an image
      if (!file.type.startsWith('image/')) {
        this.showAlert('Invalid File', 'Please select an image file.');
        return;
      }

      // Read file as base64
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64String = e.target?.result as string;
        
        // Display the image
        this.capturedImage = base64String;
        this.identificationResult = null;
        
        // Extract base64 data (remove data:image/...;base64, prefix)
        const base64Data = base64String.split(',')[1];
        
        // Create Photo object with actual filename
        const photo: Photo = {
          base64String: base64Data,
          format: file.type.split('/')[1] as any,
          saved: false
        };
        
        // Use the actual filename from the file
        console.log('Using actual filename:', file.name);
        await this.identifyDevice(photo, file.name);
      };

      reader.onerror = () => {
        this.showAlert('Read Error', 'Failed to read the selected file.');
      };

      reader.readAsDataURL(file);
      
      // Reset input so the same file can be selected again
      input.value = '';
      
    } catch (error) {
      console.error('Error processing file:', error);
      this.showAlert('File Error', 'Failed to process the selected file. Please try again.');
    }
  }

  /**
   * Send the captured image to the Python API for identification
   */
  async identifyDevice(image: Photo, filename?: string) {
    if (!image.base64String) {
      this.showToast('No image data available', 'danger');
      return;
    }

    if (!this.apiHealthy) {
      this.showToast('API is not available. Please check the Python service.', 'danger');
      return;
    }

    const loading = await this.loadingController.create({
      message: 'Diagnosing internet issue...',
      spinner: 'crescent'
    });

    try {
      await loading.present();
      this.isLoading = true;

      // Convert base64 to blob
      const imageBlob = this.deviceService.base64ToBlob(image.base64String);
      
      // Use provided filename or generate one with timestamp
      const finalFilename = filename || `camera_capture_${Date.now()}.jpg`;
      
      // Send to API
      const result = await firstValueFrom(this.deviceService.identifyDevice(imageBlob, finalFilename));
      
      if (result) {
        this.identificationResult = result;
        
        if (result.status === 'success') {
          //this.showToast(`Device identified: ${result.top_prediction?.label}`, 'success');
          this.showToast(`Problem identified: ${result.problem_description}`, 'danger');
        } else if (result.status === 'model_loading') {
          this.showToast(`Model is loading. Please wait ${result.estimated_time}s and try again.`, 'warning');
        } else {
          this.showToast(result.message || 'Unable to identify device', 'warning');
        }
      }

    } catch (error: any) {
      console.error('Error identifying device:', error);
      
      let errorMessage = 'Failed to identify device. ';
      if (error.status === 0) {
        errorMessage += 'Cannot connect to API. Make sure the Python service is running.';
      } else if (error.error?.detail) {
        errorMessage += error.error.detail;
      } else {
        errorMessage += 'Please try again.';
      }
      
      this.showAlert('Identification Error', errorMessage);
    } finally {
      this.isLoading = false;
      await loading.dismiss();
    }
  }

  /**
   * Clear the current image and results
   */
  clearImage() {
    this.capturedImage = null;
    this.identificationResult = null;
  }

  /**
   * Get confidence percentage as a formatted string
   */
  getConfidencePercent(score: number): string {
    return (score * 100).toFixed(1) + '%';
  }

  /**
   * Get color for confidence score
   */
  getConfidenceColor(score: number): string {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'danger';
  }

  /**
   * Show a toast message
   */
  async showToast(message: string, color: 'success' | 'warning' | 'danger' | 'dark' = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      color,
      position: 'bottom'
    });
    toast.present();
  }

  /**
   * Show an alert dialog
   */
  async showAlert(header: string, message: string) {
    const alert = await this.alertController.create({
      header,
      message,
      buttons: ['OK']
    });
    await alert.present();
  }
}
