//------------------------------------------------------------------------------
// Autor: Luis Enrique Coronado Zuniga
// You are free to use, change, or redistribute the code in any way you wish
// but please maintain the name of the original author.
// This code comes with no warranty of any kind.

// ****************************** Description ************************************





// This program is based in the tools of the Kinect SDK from Microsoft Corporation.
//-------------------------------------------------------------------------------

namespace Microsoft.Samples.Kinect.FaceBasics
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Diagnostics;
    using System.Globalization;
    using System.IO;
    using System.Windows;
    using System.Windows.Media;
    using System.Windows.Media.Imaging;
    using System.Windows.Media.Media3D;
    using System.Resources;
    using Microsoft.Kinect;
    using Microsoft.Kinect.Face;
    using System.Web.Script.Serialization;
 

    // Libraries added
    using System.Windows.Controls;
    using System.Threading;
   
    /// <summary>
    /// Interaction logic for MainWindow
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        
        

        public class Sound
        {
            public float beam = 0; //(6) todo
            public float angle = 0; //(7) 
            public float confidence = 0; //(17) 
        }


        public class Human
        {

            // Other relevant features
            public double shoulder_rot = 0;  //radians (1)
            public double hip_rot = 0; //radians  (10) 

            public float[] pedes_pos = { 0, 0, 0 }; //pedestrian position (3,21), in this moment is equal to SpineMid
            //public float[] pedes_vel = { 0, 0, 0 }; // pedestrian veloccity (2) todo in python

            // Body variables (Marko thesis)
            public float[] ShoulderLeft = { 0, 0, 0 };
            public float[] ShoulderRight = { 0, 0, 0 };
            public float[] SpineBase = { 0, 0, 0 };
            public float[] SpineMid = { 0, 0, 0 }; //(8,9)
            public float[] SpineShoulder = { 0, 0, 0 };
            public float[] WristLeft = { 0, 0, 0 };
            public float[] WristRight = { 0, 0, 0 };
            public float[] ElbowLeft = { 0, 0, 0 };
            public float[] ElbowRight = { 0, 0, 0 };
            public float[] HipLeft = { 0, 0, 0 };
            public float[] HipRight = { 0, 0, 0 };
            public float[] Neck = { 0, 0, 0 };

            //This variable represent the face position
            public float[] Head = { 0, 0, 0 }; //(5) but in the pepper is in pixels

            // Face rotation definition: pitch, yaw, roll
            public int face_yaw = 0;
            public int face_pitch = 0;
            public int face_roll = 0;

            public string face_happy = "ukn";
            public string face_engaged = "ukn";
            public string face_glasses = "ukn";
            public string face_lefteyeclosed = "ukn";
            public string face_righteyeclosed = "ukn";
            public string face_mouthopen = "ukn";
            public string face_mouthmoved = "ukn";
            public string face_lookingaway = "ukn";

            public double face_size = 0; //(4) //TODO
            public int index = 0;


        }


        // Topics and messages for comunication ******************************************************************************
        // Definition of the topics

        Sound haudio;

        bool publish_data = false;

        Publisher pub_human;
        Publisher pub_sound;

        // Frames to be send via NetMQ
        List<Human> human_state;


        
        // Interface variables *************************************************************************************************

        //Kinect --------------------

        /// <summary>
        /// Drawing group for body rendering output
        /// </summary>
        private DrawingGroup drawingGroup;

        /// <summary>
        /// Drawing image that we will display
        /// </summary>
        private DrawingImage imageSource;

        /// <summary>
        /// Active Kinect sensor
        /// </summary>
        private KinectSensor kinectSensor = null;

        /// <summary>
        /// Coordinate mapper to map one type of point to another
        /// </summary>
        private CoordinateMapper coordinateMapper = null;

        // Face ---------------------

        /// <summary>
        /// Thickness of face bounding box and face points
        /// </summary>
        private const double DrawFaceShapeThickness = 8;

        /// <summary>
        /// Font size of face property text 
        /// </summary>
        private const double DrawTextFontSize = 30;

        /// <summary>
        /// Radius of face point circle
        /// </summary>
        private const double FacePointRadius = 1.0;

        /// <summary>
        /// Text layout offset in X axis
        /// </summary>
        private const float TextLayoutOffsetX = -0.1f;
        
        /// <summary>
        /// Text layout offset in Y axis
        /// </summary>
        private const float TextLayoutOffsetY = -0.15f;

        /// <summary>
        /// Face rotation display angle increment in degrees
        /// </summary>
        private const double FaceRotationIncrementInDegrees = 5.0;

        /// <summary>
        /// Formatted text to indicate that there are no bodies/faces tracked in the FOV
        /// </summary>
        private FormattedText textFaceNotTracked = new FormattedText(
                        "No bodies or faces are tracked ...",
                        CultureInfo.GetCultureInfo("en-us"),
                        FlowDirection.LeftToRight,
                        new Typeface("Georgia"),
                        DrawTextFontSize,
                        Brushes.Black);

        /// <summary>
        /// Text layout for the no face tracked message
        /// </summary>
        private Point textLayoutFaceNotTracked = new Point(10.0, 10.0);

        /// <summary>
        /// Width of display (color space)
        /// </summary>
        private int displayWidth;

        /// <summary>
        /// Height of display (color space)
        /// </summary>
        private int displayHeight;

        /// <summary>
        /// Display rectangle
        /// </summary>
        private Rect displayRect;

        /// <summary>
        /// List of brushes for each face tracked
        /// </summary>
        private List<Brush> faceBrush;

        /// <summary>
        /// Current status text to display
        /// </summary>
        private string statusText = null;


        /// <summary>
        /// Face frame sources
        /// </summary>
        private FaceFrameSource[] faceFrameSources = null;

        /// <summary>
        /// Face frame readers
        /// </summary>
        private FaceFrameReader[] faceFrameReaders = null;

        /// <summary>
        /// Storage for face frame results
        /// </summary>
        private FaceFrameResult[] faceFrameResults = null;

        /// <summary>
        /// Reader for body frames
        /// </summary>
        private BodyFrameReader bodyFrameReader = null;

        /// <summary>
        /// Array to store bodies
        /// </summary>
        private Body[] bodies = null;

        /// <summary>
        /// Number of bodies tracked
        /// </summary>
        private int bodyCount;

        // Color RGB -------------------

        /// <summary>
        /// Reader for color frames
        /// </summary>
        private ColorFrameReader colorFrameReader = null;

        /// <summary>
        /// Bitmap to display
        /// </summary>
        private WriteableBitmap colorBitmap = null;

        // Body

        /// <summary>
        /// definition of bones
        /// </summary>
        private List<Tuple<JointType, JointType>> bones;

        /// <summary>
        /// List of colors for each body tracked
        /// </summary>
        private List<Pen> bodyColors;


        // Audio ---------------------

        /// <summary>
        /// Number of samples captured from Kinect audio stream each millisecond.
        /// </summary>
        private const int SamplesPerMillisecond = 16;

        /// <summary>
        /// Number of bytes in each Kinect audio stream sample (32-bit IEEE float).
        /// </summary>
        private const int BytesPerSample = sizeof(float);

        /// <summary>
        /// Number of audio samples represented by each column of pixels in wave bitmap.
        /// </summary>
        private const int SamplesPerColumn = 40;

        /// <summary>
        /// Minimum energy of audio to display (a negative number in dB value, where 0 dB is full scale)
        /// </summary>
        private const int MinEnergy = -90;

        /// <summary>
        /// Width of bitmap that stores audio stream energy data ready for visualization.
        /// </summary>
        private const int EnergyBitmapWidth = 780;

        /// <summary>
        /// Height of bitmap that stores audio stream energy data ready for visualization.
        /// </summary>
        private const int EnergyBitmapHeight = 195;

        /// <summary>
        /// Bitmap that contains constructed visualization for audio stream energy, ready to
        /// be displayed. It is a 2-color bitmap with white as background color and blue as
        /// foreground color.
        /// </summary>
        private readonly WriteableBitmap energyBitmap;

        /// <summary>
        /// Rectangle representing the entire energy bitmap area. Used when drawing background
        /// for energy visualization.
        /// </summary>
        private readonly Int32Rect fullEnergyRect = new Int32Rect(0, 0, EnergyBitmapWidth, EnergyBitmapHeight);

        /// <summary>
        /// Array of background-color pixels corresponding to an area equal to the size of whole energy bitmap.
        /// </summary>
        private readonly byte[] backgroundPixels = new byte[EnergyBitmapWidth * EnergyBitmapHeight];

        /// <summary>
        /// Will be allocated a buffer to hold a single sub frame of audio data read from audio stream.
        /// </summary>
        private readonly byte[] audioBuffer = null;

        /// <summary>
        /// Buffer used to store audio stream energy data as we read audio.
        /// We store 25% more energy values than we strictly need for visualization to allow for a smoother
        /// stream animation effect, since rendering happens on a different schedule with respect to audio
        /// capture.
        /// </summary>
        private readonly float[] energy = new float[(uint)(EnergyBitmapWidth * 1.25)];

        /// <summary>
        /// Object for locking energy buffer to synchronize threads.
        /// </summary>
        private readonly object energyLock = new object();


        /// <summary>
        /// Reader for audio frames
        /// </summary>
        private AudioBeamFrameReader reader = null;

        /// <summary>
        /// Last observed audio beam angle in radians, in the range [-pi/2, +pi/2]
        /// </summary>
        private float beamAngle = 0;

        /// <summary>
        /// Last observed audio beam angle confidence, in the range [0, 1]
        /// </summary>
        private float beamAngleConfidence = 0;

        /// <summary>
        /// Array of foreground-color pixels corresponding to a line as long as the energy bitmap is tall.
        /// This gets re-used while constructing the energy visualization.
        /// </summary>
        private byte[] foregroundPixels;

        /// <summary>
        /// Sum of squares of audio samples being accumulated to compute the next energy value.
        /// </summary>
        private float accumulatedSquareSum;

        /// <summary>
        /// Number of audio samples accumulated so far to compute the next energy value.
        /// </summary>
        private int accumulatedSampleCount;

        /// <summary>
        /// Index of next element available in audio energy buffer.
        /// </summary>
        private int energyIndex;

        /// <summary>
        /// Number of newly calculated audio stream energy values that have not yet been
        /// displayed.
        /// </summary>
        private int newEnergyAvailable;

        /// <summary>
        /// Error between time slice we wanted to display and time slice that we ended up
        /// displaying, given that we have to display in integer pixels.
        /// </summary>
        private float energyError;

        /// <summary>
        /// Last time energy visualization was rendered to screen.
        /// </summary>
        private DateTime? lastEnergyRefreshTime;

        /// <summary>
        /// Index of first energy element that has never (yet) been displayed to screen.
        /// </summary>
        private int energyRefreshIndex;

        // Body ---------------------------------------------------------------------


        /// <summary>
        /// Width of display (color space)
        /// </summary>
        private int DepthdisplayWidth;

        /// <summary>
        /// Height of display (color space)
        /// </summary>
        private int DepthdisplayHeight;

        /// <summary>
        /// Radius of drawn hand circles
        /// </summary>
        private const double HandSize = 30;

        /// <summary>
        /// Thickness of drawn joint lines
        /// </summary>
        private const double JointThickness = 3;

        /// <summary>
        /// Thickness of clip edge rectangles
        /// </summary>
        private const double ClipBoundsThickness = 10;

        /// <summary>
        /// Constant for clamping Z values of camera space points from being negative
        /// </summary>
        private const float InferredZPositionClamp = 0.1f;

        /// <summary>
        /// Brush used for drawing hands that are currently tracked as closed
        /// </summary>
        private readonly Brush handClosedBrush = new SolidColorBrush(Color.FromArgb(128, 255, 0, 0));

        /// <summary>
        /// Brush used for drawing hands that are currently tracked as opened
        /// </summary>
        private readonly Brush handOpenBrush = new SolidColorBrush(Color.FromArgb(128, 0, 255, 0));

        /// <summary>
        /// Brush used for drawing hands that are currently tracked as in lasso (pointer) position
        /// </summary>
        private readonly Brush handLassoBrush = new SolidColorBrush(Color.FromArgb(128, 0, 0, 255));

        /// <summary>
        /// Brush used for drawing joints that are currently tracked
        /// </summary>
        private readonly Brush trackedJointBrush = new SolidColorBrush(Color.FromArgb(255, 68, 192, 68));

        /// <summary>
        /// Brush used for drawing joints that are currently inferred
        /// </summary>        
        private readonly Brush inferredJointBrush = Brushes.Yellow;

        /// <summary>
        /// Pen used for drawing bones that are currently inferred
        /// </summary>        
        private readonly Pen inferredBonePen = new Pen(Brushes.Gray, 1);





        // RGB functions and draw functions ********************************************************************************
        /// <summary>
        /// Handles the color frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_ColorFrameArrived(object sender, ColorFrameArrivedEventArgs e)
        {
            // ColorFrame is IDisposable
            using (ColorFrame colorFrame = e.FrameReference.AcquireFrame())
            {
                if (colorFrame != null)
                {
                    FrameDescription colorFrameDescription = colorFrame.FrameDescription;

                    using (KinectBuffer colorBuffer = colorFrame.LockRawImageBuffer())
                    {
                        this.colorBitmap.Lock();

                        // verify data and write the new color frame data to the display bitmap
                        if ((colorFrameDescription.Width == this.colorBitmap.PixelWidth) && (colorFrameDescription.Height == this.colorBitmap.PixelHeight))
                        {
                            colorFrame.CopyConvertedFrameDataToIntPtr(
                                this.colorBitmap.BackBuffer,
                                (uint)(colorFrameDescription.Width * colorFrameDescription.Height * 4),
                                ColorImageFormat.Bgra);

                            this.colorBitmap.AddDirtyRect(new Int32Rect(0, 0, this.colorBitmap.PixelWidth, this.colorBitmap.PixelHeight));
                        }

                        this.colorBitmap.Unlock();
                    }
                }
            }
        }


        /// <summary>
        /// Gets the bitmap to display the RGB image
        /// </summary>
        public ImageSource ImageSource
        {
            get
            {
                return this.colorBitmap;
            }
        }

        /// <summary>
        /// Gets the bitmap to display the Face frames in a RGB image
        /// </summary>
        public ImageSource ImageSourceDraw
        {
            get
            {
                return this.imageSource;
            }
        }

        /// <summary>
        /// Gets or sets the current status text to display
        /// </summary>
        public string StatusText
        {
            get
            {
                return this.statusText;
            }

            set
            {
                if (this.statusText != value)
                {
                    this.statusText = value;

                    // notify any bound elements that the text has changed
                    if (this.PropertyChanged != null)
                    {
                        this.PropertyChanged(this, new PropertyChangedEventArgs("StatusText"));
                    }
                }
            }
        }

        // Audio functions ************************************************************************************************
        /// <summary>
        /// Handles the audio frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_AudioFrameArrived(object sender, AudioBeamFrameArrivedEventArgs e)
        {
            AudioBeamFrameReference frameReference = e.FrameReference;
            AudioBeamFrameList frameList = frameReference.AcquireBeamFrames();

            if (frameList != null)
            {
                // AudioBeamFrameList is IDisposable
                using (frameList)
                {
                    // Only one audio beam is supported. Get the sub frame list for this beam
                    IReadOnlyList<AudioBeamSubFrame> subFrameList = frameList[0].SubFrames;
                    // Loop over all sub frames, extract audio buffer and beam information
                    foreach (AudioBeamSubFrame subFrame in subFrameList)
                    {
                        this.beamAngle = subFrame.BeamAngle;
                        this.beamAngleConfidence = subFrame.BeamAngleConfidence;

                        // reset the variables before new energies are available
                        this.accumulatedSquareSum = 0;
                        this.accumulatedSampleCount = 0;

                        for (int i = 0; i < this.audioBuffer.Length; i += sizeof(float))
                        {
                            // Extract the 32-bit IEEE float sample from the byte array
                            float audioSample = BitConverter.ToSingle(this.audioBuffer, i);

                            this.accumulatedSquareSum += audioSample * audioSample;
                            ++this.accumulatedSampleCount;

                            if (this.accumulatedSampleCount < 40)
                            {
                                continue;
                            }

                        }

                    }
                }
            }
        }

       
        /// INotifyPropertyChangedPropertyChanged event to allow window controls to bind to changeable data
        public event PropertyChangedEventHandler PropertyChanged;



        // Face functions ****************************************************************************************************

        /// <summary>
        /// Converts rotation quaternion to Euler angles 
        /// And then maps them to a specified range of values to control the refresh rate
        /// </summary>
        /// <param name="rotQuaternion">face rotation quaternion</param>
        /// <param name="pitch">rotation about the X-axis</param>
        /// <param name="yaw">rotation about the Y-axis</param>
        /// <param name="roll">rotation about the Z-axis</param>
        private static void ExtractFaceRotationInDegrees(Vector4 rotQuaternion, out int pitch, out int yaw, out int roll)
        {
            double x = rotQuaternion.X;
            double y = rotQuaternion.Y;
            double z = rotQuaternion.Z;
            double w = rotQuaternion.W;

            // convert face rotation quaternion to Euler angles in degrees
            double yawD, pitchD, rollD;
            pitchD = Math.Atan2(2 * ((y * z) + (w * x)), (w * w) - (x * x) - (y * y) + (z * z)) / Math.PI * 180.0;
            yawD = Math.Asin(2 * ((w * y) - (x * z))) / Math.PI * 180.0;
            rollD = Math.Atan2(2 * ((x * y) + (w * z)), (w * w) + (x * x) - (y * y) - (z * z)) / Math.PI * 180.0;

            // clamp the values to a multiple of the specified increment to control the refresh rate
            double increment = FaceRotationIncrementInDegrees;
            pitch = (int)(Math.Floor((pitchD + ((increment / 2.0) * (pitchD > 0 ? 1.0 : -1.0))) / increment) * increment);
            yaw = (int)(Math.Floor((yawD + ((increment / 2.0) * (yawD > 0 ? 1.0 : -1.0))) / increment) * increment);
            roll = (int)(Math.Floor((rollD + ((increment / 2.0) * (rollD > 0 ? 1.0 : -1.0))) / increment) * increment);
        }


        /// <summary>
        /// Handles the face frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_FaceFrameArrived(object sender, FaceFrameArrivedEventArgs e)
        {
            using (FaceFrame faceFrame = e.FrameReference.AcquireFrame())
            {
                if (faceFrame != null)
                {
                    // get the index of the face source from the face source array
                    int index = this.GetFaceSourceIndex(faceFrame.FaceFrameSource);

                    // check if this face frame has valid face frame results
                    if (this.ValidateFaceBoxAndPoints(faceFrame.FaceFrameResult))
                    {
                        // store this face frame result to draw later
                        this.faceFrameResults[index] = faceFrame.FaceFrameResult;
                    }
                    else
                    {
                        // indicates that the latest face frame result from this reader is invalid
                        this.faceFrameResults[index] = null;
                    }
                }
            }
        }

        /// <summary>
        /// Returns the index of the face frame source
        /// </summary>
        /// <param name="faceFrameSource">the face frame source</param>
        /// <returns>the index of the face source in the face source array</returns>
        private int GetFaceSourceIndex(FaceFrameSource faceFrameSource)
        {
            int index = -1;

            for (int i = 0; i < this.bodyCount; i++)
            {
                if (this.faceFrameSources[i] == faceFrameSource)
                {
                    index = i;
                    break;
                }
            }

            return index;
        }


        // Body functions **********************************************************************************************************

        /// <summary>
        /// Draws a body
        /// </summary>
        /// <param name="joints">joints to draw</param>
        /// <param name="jointPoints">translated positions of joints to draw</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        /// <param name="drawingPen">specifies color to draw a specific body</param>
        private void DrawBody(IReadOnlyDictionary<JointType, Joint> joints, IDictionary<JointType, Point> jointPoints, DrawingContext drawingContext, Pen drawingPen)
        {
            // Draw the bones
            foreach (var bone in this.bones)
            {
                this.DrawBone(joints, jointPoints, bone.Item1, bone.Item2, drawingContext, drawingPen);
            }

            // Draw the joints
            foreach (JointType jointType in joints.Keys)
            {
                Brush drawBrush = null;

                TrackingState trackingState = joints[jointType].TrackingState;

                if (trackingState == TrackingState.Tracked)
                {
                    drawBrush = this.trackedJointBrush;
                }
                else if (trackingState == TrackingState.Inferred)
                {
                    drawBrush = this.inferredJointBrush;
                }

                if (drawBrush != null)
                {
                    //drawingContext.DrawEllipse(drawBrush, null, jointPoints[jointType], JointThickness, JointThickness);
                }
            }
        }

        /// <summary>
        /// Draws one bone of a body (joint to joint)
        /// </summary>
        /// <param name="joints">joints to draw</param>
        /// <param name="jointPoints">translated positions of joints to draw</param>
        /// <param name="jointType0">first joint of bone to draw</param>
        /// <param name="jointType1">second joint of bone to draw</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        /// /// <param name="drawingPen">specifies color to draw a specific bone</param>
        private void DrawBone(IReadOnlyDictionary<JointType, Joint> joints, IDictionary<JointType, Point> jointPoints, JointType jointType0, JointType jointType1, DrawingContext drawingContext, Pen drawingPen)
        {
            Joint joint0 = joints[jointType0];
            Joint joint1 = joints[jointType1];

            // If we can't find either of these joints, exit
            if (joint0.TrackingState == TrackingState.NotTracked ||
                joint1.TrackingState == TrackingState.NotTracked)
            {
                return;
            }

            // We assume all drawn bones are inferred unless BOTH joints are tracked
            Pen drawPen = this.inferredBonePen;
            if ((joint0.TrackingState == TrackingState.Tracked) && (joint1.TrackingState == TrackingState.Tracked))
            {
                drawPen = drawingPen;
            }

            drawingContext.DrawLine(drawPen, jointPoints[jointType0], jointPoints[jointType1]);
        }

        /// <summary>
        /// Draws a hand symbol if the hand is tracked: red circle = closed, green circle = opened; blue circle = lasso
        /// </summary>
        /// <param name="handState">state of the hand</param>
        /// <param name="handPosition">position of the hand</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        private void DrawHand(HandState handState, Point handPosition, DrawingContext drawingContext)
        {
            switch (handState)
            {
                case HandState.Closed:
                    drawingContext.DrawEllipse(this.handClosedBrush, null, handPosition, HandSize, HandSize);
                    break;

                case HandState.Open:
                    drawingContext.DrawEllipse(this.handOpenBrush, null, handPosition, HandSize, HandSize);
                    break;

                case HandState.Lasso:
                    drawingContext.DrawEllipse(this.handLassoBrush, null, handPosition, HandSize, HandSize);
                    break;
            }
        }

        /// <summary>
        /// Draws indicators to show which edges are clipping body data
        /// </summary>
        /// <param name="body">body to draw clipping information for</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        private void DrawClippedEdges(Body body, DrawingContext drawingContext)
        {
            FrameEdges clippedEdges = body.ClippedEdges;

            if (clippedEdges.HasFlag(FrameEdges.Bottom))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, this.displayHeight - ClipBoundsThickness, this.displayWidth, ClipBoundsThickness));
            }

            if (clippedEdges.HasFlag(FrameEdges.Top))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, this.displayWidth, ClipBoundsThickness));
            }

            if (clippedEdges.HasFlag(FrameEdges.Left))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, ClipBoundsThickness, this.displayHeight));
            }

            if (clippedEdges.HasFlag(FrameEdges.Right))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(this.displayWidth - ClipBoundsThickness, 0, ClipBoundsThickness, this.displayHeight));
            }
        }

        /// <summary>
        /// Handles the body frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_BodyFrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            using (var bodyFrame = e.FrameReference.AcquireFrame())
            {
                if (bodyFrame != null)
                {
                    // update body data
                    bodyFrame.GetAndRefreshBodyData(this.bodies);

                    using (DrawingContext dc = this.drawingGroup.Open())
                    {
                        // draw the trasparent background
                        dc.DrawRectangle(Brushes.Transparent, null, this.displayRect);

                        // Face drawing ***********************************************************************
                        bool drawFaceResult = false;

                        // iterate through each face source
                        for (int i = 0; i < this.bodyCount; i++)
                        {
                            // check if a valid face is tracked in this face source
                            if (this.faceFrameSources[i].IsTrackingIdValid)
                            {
                                // check if we have valid face frame results
                                if (this.faceFrameResults[i] != null)
                                {
                                    // draw and get the face frame results
                                    this.DrawFaceFrameResults(i, this.faceFrameResults[i], dc);
                                    
                                    if (!drawFaceResult)
                                    {
                                        drawFaceResult = true;
                                    }
                                }
                            }
                            else
                            {
                                // check if the corresponding body is tracked 
                                if (this.bodies[i].IsTracked)
                                {
                                    // update the face frame source to track this body
                                    this.faceFrameSources[i].TrackingId = this.bodies[i].TrackingId;
                                }
                            }
                        }

                        if (!drawFaceResult)
                        {
                            // if no faces were drawn then this indicates one of the following:
                            // a body was not tracked 
                            // a body was tracked but the corresponding face was not tracked
                            // a body and the corresponding face was tracked though the face box or the face points were not valid
                            dc.DrawText(
                                this.textFaceNotTracked, 
                                this.textLayoutFaceNotTracked);
                        }

                        this.drawingGroup.ClipGeometry = new RectangleGeometry(this.displayRect);
                    }
                }
            }
        }

        private void body_info(int faceindex, DrawingContext dc, Body body)
        {
            Pen drawPen = this.bodyColors[faceindex];

            if (body.IsTracked)
            {
                //this.DrawClippedEdges(body, dc);

                IReadOnlyDictionary<JointType, Joint> joints = body.Joints;

                // convert the joint points to depth (display) space
                Dictionary<JointType, Point> jointPoints = new Dictionary<JointType, Point>();

                foreach (JointType jointType in joints.Keys)
                {
                    // sometimes the depth(Z) of an inferred joint may show as negative
                    // clamp down to 0.1f to prevent coordinatemapper from returning (-Infinity, -Infinity)
                    CameraSpacePoint position = joints[jointType].Position;
                    if (position.Z < 0)
                    {
                        position.Z = InferredZPositionClamp;
                    }

                    DepthSpacePoint depthSpacePoint = this.coordinateMapper.MapCameraPointToDepthSpace(position);
                    jointPoints[jointType] = new Point(depthSpacePoint.X, depthSpacePoint.Y);

                    if (jointType == JointType.SpineMid)
                    {

                        human_state[faceindex].pedes_pos[0] = position.X;
                        human_state[faceindex].pedes_pos[1] = position.Y;
                        human_state[faceindex].pedes_pos[2] = position.Z;

                        human_state[faceindex].SpineMid[0] = position.X;
                        human_state[faceindex].SpineMid[1] = position.Y;
                        human_state[faceindex].SpineMid[2] = position.Z;
                    }

                    if (jointType == JointType.ShoulderLeft)
                    {
                        human_state[faceindex].ShoulderLeft[0] = position.X;
                        human_state[faceindex].ShoulderLeft[1] = position.Y;
                        human_state[faceindex].ShoulderLeft[2] = position.Z;
                    }


                    if (jointType == JointType.ShoulderRight)
                    {
                        human_state[faceindex].ShoulderRight[0] = position.X;
                        human_state[faceindex].ShoulderRight[1] = position.Y;
                        human_state[faceindex].ShoulderRight[2] = position.Z;
                    }

                    if (jointType == JointType.SpineBase)
                    {
                        human_state[faceindex].SpineBase[0] = position.X;
                        human_state[faceindex].SpineBase[1] = position.Y;
                        human_state[faceindex].SpineBase[2] = position.Z;
                    }

                    if (jointType == JointType.SpineShoulder)
                    {
                        human_state[faceindex].SpineShoulder[0] = position.X;
                        human_state[faceindex].SpineShoulder[1] = position.Y;
                        human_state[faceindex].SpineShoulder[2] = position.Z;
                    }


                    if (jointType == JointType.WristLeft)
                    {
                        human_state[faceindex].WristLeft[0] = position.X;
                        human_state[faceindex].WristLeft[1] = position.Y;
                        human_state[faceindex].WristLeft[2] = position.Z;
                    }

                    if (jointType == JointType.WristRight)
                    {
                        human_state[faceindex].WristRight[0] = position.X;
                        human_state[faceindex].WristRight[1] = position.Y;
                        human_state[faceindex].WristRight[2] = position.Z;
                    }

                    if (jointType == JointType.ElbowLeft)
                    {
                        human_state[faceindex].ElbowLeft[0] = position.X;
                        human_state[faceindex].ElbowLeft[1] = position.Y;
                        human_state[faceindex].ElbowLeft[2] = position.Z;
                    }


                    if (jointType == JointType.ElbowRight)
                    {
                        human_state[faceindex].ElbowRight[0] = position.X;
                        human_state[faceindex].ElbowRight[1] = position.Y;
                        human_state[faceindex].ElbowRight[2] = position.Z;
                    }

                    if (jointType == JointType.HipLeft)
                    {
                        human_state[faceindex].HipLeft[0] = position.X;
                        human_state[faceindex].HipLeft[1] = position.Y;
                        human_state[faceindex].HipLeft[2] = position.Z;
                    }

                    if (jointType == JointType.ElbowRight)
                    {
                        human_state[faceindex].ElbowRight[0] = position.X;
                        human_state[faceindex].ElbowRight[1] = position.Y;
                        human_state[faceindex].ElbowRight[2] = position.Z;
                    }

                    if (jointType == JointType.HipLeft)
                    {
                        human_state[faceindex].HipLeft[0] = position.X;
                        human_state[faceindex].HipLeft[1] = position.Y;
                        human_state[faceindex].HipLeft[2] = position.Z;
                    }

                    if (jointType == JointType.HipRight)
                    {
                        human_state[faceindex].HipRight[0] = position.X;
                        human_state[faceindex].HipRight[1] = position.Y;
                        human_state[faceindex].HipRight[2] = position.Z;
                    }

                    if (jointType == JointType.HipRight)
                    {
                        human_state[faceindex].HipRight[0] = position.X;
                        human_state[faceindex].HipRight[1] = position.Y;
                        human_state[faceindex].HipRight[2] = position.Z;
                    }


                    if (jointType == JointType.Neck)
                    {
                        human_state[faceindex].Neck[0] = position.X;
                        human_state[faceindex].Neck[1] = position.Y;
                        human_state[faceindex].Neck[2] = position.Z;
                    }

                    if (jointType == JointType.Head)
                    {
                        human_state[faceindex].Head[0] = position.X;
                        human_state[faceindex].Head[1] = position.Y;
                        human_state[faceindex].Head[2] = position.Z;
                    }

                    // Here we tranfrom the coordinates to color space to be sincronized with the image ------------- IMPORTANT
                    ColorSpacePoint colorSpacePoint = this.coordinateMapper.MapCameraPointToColorSpace(position);
                    jointPoints[jointType] = new Point(colorSpacePoint.X, colorSpacePoint.Y);

                }

                // Calculate sholuder and hip rotations
                human_state[faceindex].shoulder_rot = Math.Atan2((human_state[faceindex].ShoulderRight[2] - human_state[faceindex].ShoulderLeft[2]), (human_state[faceindex].ShoulderRight[0] - human_state[faceindex].ShoulderLeft[0]));
                human_state[faceindex].hip_rot = Math.Atan2((human_state[faceindex].HipRight[2] - human_state[faceindex].HipLeft[2]), (human_state[faceindex].HipRight[0] - human_state[faceindex].HipLeft[0]));

                double angle = Math.Round(human_state[faceindex].shoulder_rot * (180 / Math.PI));
                text_testShoulder.Content = "Shoulder rotation =" + angle.ToString() + "°";

                angle = Math.Round(human_state[faceindex].hip_rot * (180 / Math.PI));
                text_testHip.Content = "Hip rotation =" + angle.ToString() + "°";

                if (publish_data == true)
                {
                    publish_human_states(faceindex);
                }

                this.DrawBody(joints, jointPoints, dc, drawPen);
                this.DrawHand(body.HandLeftState, jointPoints[JointType.HandLeft], dc);
                this.DrawHand(body.HandRightState, jointPoints[JointType.HandRight], dc);
            }


        }

        /// <summary>
        /// Computes the face result text position by adding an offset to the corresponding 
        /// body's head joint in camera space and then by projecting it to screen space
        /// </summary>
        /// <param name="faceIndex">the index of the face frame corresponding to a specific body in the FOV</param>
        /// <param name="faceTextLayout">the text layout position in screen space</param>
        /// <returns>success or failure</returns>
        private bool GetFaceTextPositionInColorSpace(int faceIndex, out Point faceTextLayout, DrawingContext dc)
        {
            faceTextLayout = new Point();
            bool isLayoutValid = false;

            Body body = this.bodies[faceIndex];

            body_info(faceIndex, dc, body);

            if (body.IsTracked)
            {
                var headJoint = body.Joints[JointType.Head].Position;

                CameraSpacePoint textPoint = new CameraSpacePoint()
                {
                    X = headJoint.X + TextLayoutOffsetX,
                    Y = headJoint.Y + TextLayoutOffsetY,
                    Z = headJoint.Z
                };

                ColorSpacePoint textPointInColor = this.coordinateMapper.MapCameraPointToColorSpace(textPoint);

                faceTextLayout.X = textPointInColor.X;
                faceTextLayout.Y = textPointInColor.Y;
                isLayoutValid = true;                
            }

            return isLayoutValid;
        }

        /// <summary>
        /// Validates face bounding box and face points to be within screen space
        /// </summary>
        /// <param name="faceResult">the face frame result containing face box and points</param>
        /// <returns>success or failure</returns>
        private bool ValidateFaceBoxAndPoints(FaceFrameResult faceResult)
        {
            bool isFaceValid = faceResult != null;

            if (isFaceValid)
            {
                var faceBox = faceResult.FaceBoundingBoxInColorSpace;
                if (faceBox != null)
                {
                    // check if we have a valid rectangle within the bounds of the screen space
                    isFaceValid = (faceBox.Right - faceBox.Left) > 0 &&
                                  (faceBox.Bottom - faceBox.Top) > 0 &&
                                  faceBox.Right <= this.displayWidth &&
                                  faceBox.Bottom <= this.displayHeight;

                    if (isFaceValid)
                    {
                        var facePoints = faceResult.FacePointsInColorSpace;
                        if (facePoints != null)
                        {
                            foreach (PointF pointF in facePoints.Values)
                            {
                                // check if we have a valid face point within the bounds of the screen space
                                bool isFacePointValid = pointF.X > 0.0f &&
                                                        pointF.Y > 0.0f &&
                                                        pointF.X < this.displayWidth &&
                                                        pointF.Y < this.displayHeight;

                                if (!isFacePointValid)
                                {
                                    isFaceValid = false;
                                    break;
                                }
                            }
                        }
                    }
                }
            }

            return isFaceValid;
        }



        // TODO: maybe put this in a function
        /// <summary>
        /// Draws face frame results, also get the face states and save these infromation in a set of variables.
        /// This information can be published with the publish_face_states funtion
        /// </summary>
        /// <param name="faceIndex">the index of the face frame corresponding to a specific body in the FOV</param>
        /// <param name="faceResult">container of all face frame results</param>
        /// <param name="drawingContext">drawing context to render to</param>



        /// <summary>
        /// Draws face frame results, also get the face states and save these infromation in a set of variables.
        /// This information can be published with the publish_face_states funtion
        /// </summary>
        /// <param name="faceIndex">the index of the face frame corresponding to a specific body in the FOV</param>
        /// <param name="faceResult">container of all face frame results</param>
        /// <param name="drawingContext">drawing context to render to</param>
        private void DrawFaceFrameResults(int faceIndex, FaceFrameResult faceResult, DrawingContext drawingContext)
        {
            // choose the brush based on the face index
            Brush drawingBrush = this.faceBrush[0];
            if (faceIndex < this.bodyCount)
            {
                drawingBrush = this.faceBrush[faceIndex];
            }

            Pen drawingPen = new Pen(drawingBrush, DrawFaceShapeThickness);

            // draw the face bounding box
            var faceBoxSource = faceResult.FaceBoundingBoxInColorSpace;
            Rect faceBox = new Rect(faceBoxSource.Left, faceBoxSource.Top, faceBoxSource.Right - faceBoxSource.Left, faceBoxSource.Bottom - faceBoxSource.Top);
            drawingContext.DrawRectangle(null, drawingPen, faceBox);

            if (faceResult.FacePointsInColorSpace != null)
            {
                // draw each face point
                foreach (PointF pointF in faceResult.FacePointsInColorSpace.Values)
                {
                   // drawingContext.DrawEllipse(null, drawingPen, new Point(pointF.X, pointF.Y), FacePointRadius, FacePointRadius);
                }
            }

            string faceText = string.Empty;

            // extract each face property information and store it in faceText
            if (faceResult.FaceProperties != null)
            {
                foreach (var item in faceResult.FaceProperties)
                {
                    string propertie = item.Key.ToString();
                    string face_state = "unknown";

                    // TODO: this can be simplified putting some operations in a function, is no so quickly as in Python
                    // If the propertie is happy detector, set the state
                    if (String.Compare(propertie, "Happy") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_happy = face_state;
                    }

                    // If the propertie is engaged detector, set the state
                    if (String.Compare(propertie, "Engaged") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_engaged = face_state;
                        faceText += "engaged = " + face_state + "\n";
                    }

                    // If the propertie is glasses detector, set the state
                    if (String.Compare(propertie, "WearingGlasses") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_glasses = face_state;
                    }

                    // If the propertie is left eye closed detector, set the state
                    if (String.Compare(propertie, "LeftEyeClosed") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_lefteyeclosed = face_state;
                    }

                    // If the propertie is rigth eye closed detector, set the state
                    if (String.Compare(propertie, "RightEyeClosed") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_righteyeclosed = face_state;
                    }


                    // If the propertie is rigth mouth open detector, set the state
                    if (String.Compare(propertie, "MouthOpen") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_mouthopen = face_state;
                    }


                    // If the propertie is rigth mouth moved detector, set the state
                    if (String.Compare(propertie, "MouthMoved") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_mouthmoved = face_state;
                    }

                    // If the propertie is rigth Looking Away detector, set the state
                    if (String.Compare(propertie, "LookingAway") == 0)
                    {
                        face_state = "unknown";
                        if (item.Value != DetectionResult.Unknown)
                        {
                            if (item.Value == DetectionResult.Maybe || item.Value == DetectionResult.No)
                            {
                                face_state = "no";
                            }
                            else
                            {
                                face_state = "yes";
                            }
                        }
                        human_state[faceIndex].face_lookingaway = face_state;
                        faceText += "LookingAway = " + face_state + "\n";
                    }

                    human_state[faceIndex].face_size = 0;
                  
                }
            }

            // Extract face rotation in degrees as Euler angles
            if (faceResult.FaceRotationQuaternion != null)
            {

                ExtractFaceRotationInDegrees(faceResult.FaceRotationQuaternion, out  human_state[faceIndex].face_pitch, out  human_state[faceIndex].face_yaw, out  human_state[faceIndex].face_roll);

            }

            faceText += "ID =" + faceIndex.ToString() +  "\n";

            // Render the face property and face rotation information
            Point faceTextLayout;
            if (this.GetFaceTextPositionInColorSpace(faceIndex, out faceTextLayout, drawingContext))
            {
                drawingContext.DrawText(
                        new FormattedText(
                            faceText,
                            CultureInfo.GetCultureInfo("en-us"),
                            FlowDirection.LeftToRight,
                            new Typeface("Georgia"),
                            DrawTextFontSize,
                            drawingBrush),
                        faceTextLayout);
            }
        }

        // Geeneral kinect functions **********************************************************************************

        /// <summary>
        /// Handles the event which the sensor becomes unavailable (E.g. paused, closed, unplugged).
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Sensor_IsAvailableChanged(object sender, IsAvailableChangedEventArgs e)
        {
            if (this.kinectSensor != null)
            {
                // on failure, set the status text
                this.StatusText = this.kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                                : Properties.Resources.SensorNotAvailableStatusText;
            }
        }

        // Interface functions *****************************************************************************************

        /// <summary>
        /// Execute start up tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {

            for (int i = 0; i < this.bodyCount; i++)
            {
                if (this.faceFrameReaders[i] != null)
                {
                    // wire handler for face frame arrival
                    this.faceFrameReaders[i].FrameArrived += this.Reader_FaceFrameArrived;
                }
            }

            //Add new face and body event

            if (this.bodyFrameReader != null)
            {
                // wire handler for body frame arrival
                this.bodyFrameReader.FrameArrived += this.Reader_BodyFrameArrived;
            }

            //Add new color event

            if (this.colorFrameReader != null)
            {
                // wire handler for body frame arrival
                this.colorFrameReader.FrameArrived += this.Reader_ColorFrameArrived;
            }


            // Audio
            // Initialize foreground pixels
            this.foregroundPixels = new byte[EnergyBitmapHeight];
            for (int i = 0; i < this.foregroundPixels.Length; ++i)
            {
                this.foregroundPixels[i] = 0xff;
            }

            this.waveDisplay.Source = this.energyBitmap;

            CompositionTarget.Rendering += this.UpdateEnergy;

            if (this.reader != null)
            {
                // Subscribe to new audio frame arrived events
                this.reader.FrameArrived += this.Reader_FrameArrived;
            }

            documentation.Items.Add("ZQM TOPICS");
            documentation.Items.Add("/kinect_human");
            documentation.Items.Add("/kinect_sound");


        }


        // AUDIO **********************************************************************************


        /// <summary>
        /// Handles the audio frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_FrameArrived(object sender, AudioBeamFrameArrivedEventArgs e)
        {
            AudioBeamFrameReference frameReference = e.FrameReference;
            AudioBeamFrameList frameList = frameReference.AcquireBeamFrames();

            if (frameList != null)
            {
                // AudioBeamFrameList is IDisposable
                using (frameList)
                {
                    // Only one audio beam is supported. Get the sub frame list for this beam
                    IReadOnlyList<AudioBeamSubFrame> subFrameList = frameList[0].SubFrames;

                    // Loop over all sub frames, extract audio buffer and beam information
                    foreach (AudioBeamSubFrame subFrame in subFrameList)
                    {
                        // Check if beam angle and/or confidence have changed
                        bool updateBeam = false;

                        if (subFrame.BeamAngle != this.beamAngle)
                        {
                            this.beamAngle = subFrame.BeamAngle;
                            updateBeam = true;
                        }

                        if (subFrame.BeamAngleConfidence != this.beamAngleConfidence)
                        {
                            this.beamAngleConfidence = subFrame.BeamAngleConfidence;
                            updateBeam = true;
                        }

                        if (updateBeam)
                        {
                            // Refresh display of audio beam
                            this.AudioBeamChanged();
                        }

                        // Process audio buffer
                        subFrame.CopyFrameDataToArray(this.audioBuffer);

                        for (int i = 0; i < this.audioBuffer.Length; i += BytesPerSample)
                        {
                            // Extract the 32-bit IEEE float sample from the byte array
                            float audioSample = BitConverter.ToSingle(this.audioBuffer, i);

                            this.accumulatedSquareSum += audioSample * audioSample;
                            ++this.accumulatedSampleCount;

                            if (this.accumulatedSampleCount < SamplesPerColumn)
                            {
                                continue;
                            }

                            float meanSquare = this.accumulatedSquareSum / SamplesPerColumn;

                            if (meanSquare > 1.0f)
                            {
                                // A loud audio source right next to the sensor may result in mean square values
                                // greater than 1.0. Cap it at 1.0f for display purposes.
                                meanSquare = 1.0f;
                            }

                            // Calculate energy in dB, in the range [MinEnergy, 0], where MinEnergy < 0
                            float energy = MinEnergy;

                            if (meanSquare > 0)
                            {
                                energy = (float)(10.0 * Math.Log10(meanSquare));
                            }

                            lock (this.energyLock)
                            {
                                // Normalize values to the range [0, 1] for display
                                this.energy[this.energyIndex] = (MinEnergy - energy) / MinEnergy;
                                this.energyIndex = (this.energyIndex + 1) % this.energy.Length;
                                ++this.newEnergyAvailable;
                            }

                            this.accumulatedSquareSum = 0;
                            this.accumulatedSampleCount = 0;
                        }
                    }
                }
            }
        }

        /// <summary>
        /// Method called when audio beam angle and/or confidence have changed.
        /// </summary>
        private void AudioBeamChanged()
        {
            // Maximum possible confidence corresponds to this gradient width
            const float MinGradientWidth = 0.04f;

            // Set width of mark based on confidence.
            // A confidence of 0 would give us a gradient that fills whole area diffusely.
            // A confidence of 1 would give us the narrowest allowed gradient width.
            float halfWidth = Math.Max(1 - this.beamAngleConfidence, MinGradientWidth) / 2;

            // Update the gradient representing sound source position to reflect confidence
            this.beamBarGsPre.Offset = Math.Max(this.beamBarGsMain.Offset - halfWidth, 0);
            this.beamBarGsPost.Offset = Math.Min(this.beamBarGsMain.Offset + halfWidth, 1);

            // Convert from radians to degrees for display purposes
            float beamAngleInDeg = this.beamAngle * 180.0f / (float)Math.PI;

            // Rotate gradient to match angle
            beamBarRotation.Angle = -beamAngleInDeg;
            beamNeedleRotation.Angle = -beamAngleInDeg;

            // Display new numerical values
            haudio.angle = beamAngleInDeg;
            haudio.confidence = beamAngleConfidence;
            beamAngleText.Text =  beamAngleInDeg.ToString("0", CultureInfo.CurrentCulture);
            beamConfidenceText.Text =  beamAngleConfidence.ToString("0.00", CultureInfo.CurrentCulture);
        }

        /// <summary>
        /// Handles rendering energy visualization into a bitmap.
        /// </summary>
        /// <param name="sender">object sending the event.</param>
        /// <param name="e">event arguments.</param>
        private void UpdateEnergy(object sender, EventArgs e)
        {
            lock (this.energyLock)
            {
                // Calculate how many energy samples we need to advance since the last update in order to
                // have a smooth animation effect
                DateTime now = DateTime.UtcNow;
                DateTime? previousRefreshTime = this.lastEnergyRefreshTime;
                this.lastEnergyRefreshTime = now;

                // No need to refresh if there is no new energy available to render
                if (this.newEnergyAvailable <= 0)
                {
                    return;
                }

                if (previousRefreshTime != null)
                {
                    float energyToAdvance = this.energyError + (((float)(now - previousRefreshTime.Value).TotalMilliseconds * SamplesPerMillisecond) / SamplesPerColumn);
                    int energySamplesToAdvance = Math.Min(this.newEnergyAvailable, (int)Math.Round(energyToAdvance));
                    this.energyError = energyToAdvance - energySamplesToAdvance;
                    this.energyRefreshIndex = (this.energyRefreshIndex + energySamplesToAdvance) % this.energy.Length;
                    this.newEnergyAvailable -= energySamplesToAdvance;
                }

                // clear background of energy visualization area
                this.energyBitmap.WritePixels(this.fullEnergyRect, this.backgroundPixels, EnergyBitmapWidth, 0); 

                // Draw each energy sample as a centered vertical bar, where the length of each bar is
                // proportional to the amount of energy it represents.
                // Time advances from left to right, with current time represented by the rightmost bar.
                int baseIndex = (this.energyRefreshIndex + this.energy.Length - EnergyBitmapWidth) % this.energy.Length;
                for (int i = 0; i < EnergyBitmapWidth; ++i)
                {
                    const int HalfImageHeight = EnergyBitmapHeight / 2;

                    // Each bar has a minimum height of 1 (to get a steady signal down the middle) and a maximum height
                    // equal to the bitmap height.
                    int barHeight = (int)Math.Max(1.0, this.energy[(baseIndex + i) % this.energy.Length] * EnergyBitmapHeight);

                    // Center bar vertically on image
                    var barRect = new Int32Rect(i, HalfImageHeight - (barHeight / 2), 1, barHeight);

                    // Draw bar in foreground color
                    this.energyBitmap.WritePixels(barRect, this.foregroundPixels, 1, 0); 
                }
            }
        }



        /// Initializes a new instance of the MainWindow class.**************************************
        public MainWindow()
        {


            //Human state decription

            human_state = new List<Human>();

            // 6 human frames
            human_state.Add(new Human());
            human_state.Add(new Human());
            human_state.Add(new Human());
            human_state.Add(new Human());
            human_state.Add(new Human());
            human_state.Add(new Human());

            haudio = new Sound();

            // GENERAL KINECT DESCRIPTION ********************

            // one sensor is currently supported
            this.kinectSensor = KinectSensor.GetDefault();

            // get the coordinate mapper
            this.coordinateMapper = this.kinectSensor.CoordinateMapper;

            // COLOR CAMERA ************************************

            // open the reader for the color frames
            this.colorFrameReader = this.kinectSensor.ColorFrameSource.OpenReader();

            // wire handler for frame arrival
            this.colorFrameReader.FrameArrived += this.Reader_ColorFrameArrived;

            // create the colorFrameDescription from the ColorFrameSource using Bgra format
            FrameDescription colorFrameDescription = this.kinectSensor.ColorFrameSource.CreateFrameDescription(ColorImageFormat.Bgra);

            // create the bitmap to display
            this.colorBitmap = new WriteableBitmap(colorFrameDescription.Width, colorFrameDescription.Height, 96.0, 96.0, PixelFormats.Bgr32, null);

            // FACE FRAME *****************************************

            // get the coordinate mapper
            this.coordinateMapper = this.kinectSensor.CoordinateMapper;

            // get the color frame details
            FrameDescription frameDescription = this.kinectSensor.ColorFrameSource.FrameDescription;

            // set the display specifics
            this.displayWidth = frameDescription.Width;
            this.displayHeight = frameDescription.Height;
            this.displayRect = new Rect(0.0, 0.0, this.displayWidth, this.displayHeight);

            // open the reader for the body frames
            this.bodyFrameReader = this.kinectSensor.BodyFrameSource.OpenReader();

            // wire handler for body frame arrival
            this.bodyFrameReader.FrameArrived += this.Reader_BodyFrameArrived;

            // set the maximum number of bodies that would be tracked by Kinect
            this.bodyCount = this.kinectSensor.BodyFrameSource.BodyCount;

            // allocate storage to store body objects
            this.bodies = new Body[this.bodyCount];

            // Face states definition *******

            // specify the required face frame results
            FaceFrameFeatures faceFrameFeatures =
                FaceFrameFeatures.BoundingBoxInColorSpace
                | FaceFrameFeatures.PointsInColorSpace
                | FaceFrameFeatures.RotationOrientation
                | FaceFrameFeatures.FaceEngagement
                | FaceFrameFeatures.Glasses
                | FaceFrameFeatures.Happy
                | FaceFrameFeatures.LeftEyeClosed
                | FaceFrameFeatures.RightEyeClosed
                | FaceFrameFeatures.LookingAway
                | FaceFrameFeatures.MouthMoved
                | FaceFrameFeatures.MouthOpen;

            // create a face frame source + reader to track each face in the FOV
            this.faceFrameSources = new FaceFrameSource[this.bodyCount];
            this.faceFrameReaders = new FaceFrameReader[this.bodyCount];
            for (int i = 0; i < this.bodyCount; i++)
            {
                // create the face frame source with the required face frame features and an initial tracking Id of 0
                this.faceFrameSources[i] = new FaceFrameSource(this.kinectSensor, 0, faceFrameFeatures);

                // open the corresponding reader
                this.faceFrameReaders[i] = this.faceFrameSources[i].OpenReader();
            }

            // allocate storage to store face frame results for each face in the FOV
            this.faceFrameResults = new FaceFrameResult[this.bodyCount];

            // populate face result colors - one for each face index
            this.faceBrush = new List<Brush>()
            {
                Brushes.White, 
                Brushes.Orange,
                Brushes.Green,
                Brushes.Red,
                Brushes.LightBlue,
                Brushes.Yellow
            };

            // Body and Depth frames ********************************

            //Todo sincronize face a body frames

            // get the depth (display) extents
            FrameDescription DepthframeDescription = this.kinectSensor.DepthFrameSource.FrameDescription;

            // get size of joint space
            this.DepthdisplayWidth = DepthframeDescription.Width;
            this.DepthdisplayHeight = DepthframeDescription.Height;

            // open the reader for the body frames
            this.bodyFrameReader = this.kinectSensor.BodyFrameSource.OpenReader();

            // a bone defined as a line between two joints
            this.bones = new List<Tuple<JointType, JointType>>();

            // Torso
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.Head, JointType.Neck));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.Neck, JointType.SpineShoulder));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.SpineMid));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineMid, JointType.SpineBase));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.ShoulderRight));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineShoulder, JointType.ShoulderLeft));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineBase, JointType.HipRight));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.SpineBase, JointType.HipLeft));

            // Right Arm
            this.bones.Add(new Tuple<JointType, JointType>(JointType.ShoulderRight, JointType.ElbowRight));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.ElbowRight, JointType.WristRight));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.WristRight, JointType.HandRight));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.HandRight, JointType.HandTipRight));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.WristRight, JointType.ThumbRight));

            // Left Arm
            this.bones.Add(new Tuple<JointType, JointType>(JointType.ShoulderLeft, JointType.ElbowLeft));
            this.bones.Add(new Tuple<JointType, JointType>(JointType.ElbowLeft, JointType.WristLeft));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.WristLeft, JointType.HandLeft));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.HandLeft, JointType.HandTipLeft));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.WristLeft, JointType.ThumbLeft));

            // Right Leg
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.HipRight, JointType.KneeRight));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.KneeRight, JointType.AnkleRight));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.AnkleRight, JointType.FootRight));

            // Left Leg
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.HipLeft, JointType.KneeLeft));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.KneeLeft, JointType.AnkleLeft));
            //this.bones.Add(new Tuple<JointType, JointType>(JointType.AnkleLeft, JointType.FootLeft));

            // populate body colors, one for each BodyIndex
            this.bodyColors = new List<Pen>();

            this.bodyColors.Add(new Pen(Brushes.White, 3));
            this.bodyColors.Add(new Pen(Brushes.Orange, 3));
            this.bodyColors.Add(new Pen(Brushes.Green, 3));
            this.bodyColors.Add(new Pen(Brushes.Red, 3));
            this.bodyColors.Add(new Pen(Brushes.LightBlue, 3));
            this.bodyColors.Add(new Pen(Brushes.Yellow, 3));


            // General initialization *******************************

            // Create the drawing group we'll use for drawing
            this.drawingGroup = new DrawingGroup();

            // Create an image source that we can use in our image control
            this.imageSource = new DrawingImage(this.drawingGroup);

            // set IsAvailableChanged event notifier
            this.kinectSensor.IsAvailableChanged += this.Sensor_IsAvailableChanged;

            // open the sensor
            this.kinectSensor.Open();

            // set the status text
            this.StatusText = this.kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                            : Properties.Resources.NoSensorStatusText;

            // use the window object as the view model in this simple example
            this.DataContext = this;

            if (this.kinectSensor != null)
            {
                // Open the sensor
                this.kinectSensor.Open();

                // Get its audio source
                AudioSource audioSource = this.kinectSensor.AudioSource;

                // Allocate 1024 bytes to hold a single audio sub frame. Duration sub frame 
                // is 16 msec, the sample rate is 16khz, which means 256 samples per sub frame. 
                // With 4 bytes per sample, that gives us 1024 bytes.
                this.audioBuffer = new byte[audioSource.SubFrameLengthInBytes];

                // Open the reader for the audio frames
                this.reader = audioSource.OpenReader();

                // Uncomment these two lines to overwrite the automatic mode of the audio beam.
                // It will change the beam mode to manual and set the desired beam angle.
                // In this example, point it straight forward.
                // Note that setting beam mode and beam angle will only work if the
                // application window is in the foreground.
                // Furthermore, setting these values is an asynchronous operation --
                // it may take a short period of time for the beam to adjust.
                /*
                audioSource.AudioBeams[0].AudioBeamMode = AudioBeamMode.Manual;
                audioSource.AudioBeams[0].BeamAngle = 0;
                */
            }
            else
            {
                // On failure, set the status text
                return;
            }

            this.energyBitmap = new WriteableBitmap(EnergyBitmapWidth, EnergyBitmapHeight, 96, 96, PixelFormats.Indexed1, new BitmapPalette(new List<Color> { Colors.White, Colors.Blue })); 


            // initialize the components (controls) of the window
            this.InitializeComponent();


        }

        /// <summary>
        /// Execute shutdown tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void MainWindow_Closing(object sender, CancelEventArgs e)
        {
            //Dispose body and face frames *****************
            for (int i = 0; i < this.bodyCount; i++)
            {
                if (this.faceFrameReaders[i] != null)
                {
                    // FaceFrameReader is IDisposable
                    this.faceFrameReaders[i].Dispose();
                    this.faceFrameReaders[i] = null;
                }

                if (this.faceFrameSources[i] != null)
                {
                    // FaceFrameSource is IDisposable
                    this.faceFrameSources[i].Dispose();
                    this.faceFrameSources[i] = null;
                }
            }

            //Audio reader
            CompositionTarget.Rendering -= this.UpdateEnergy;

            if (this.reader != null)
            {
                // AudioBeamFrameReader is IDisposable
                this.reader.Dispose();
                this.reader = null;
            }

            if (this.bodyFrameReader != null)
            {
                // BodyFrameReader is IDisposable
                this.bodyFrameReader.Dispose();
                this.bodyFrameReader = null;
            }

            // Dispose color frame ***********************
            if (this.colorFrameReader != null)
            {
                // ColorFrameReder is IDisposable
                this.colorFrameReader.Dispose();
                this.colorFrameReader = null;
            }

            if (this.kinectSensor != null)
            {
                this.kinectSensor.Close();
                this.kinectSensor = null;
            }

        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            pub_human = new Publisher("/kinect_human", "kinect_human", "P2P", "localhost", "9000");
            // Init publishers
            pub_sound = new Publisher("/kinect_sound", "kinect_sound", "P2P", "localhost", "9000");
            publish_data = true;
        }

        /// <summary>
        // Function used to send the body state using ZMQ socket 
        /// </summary>
        /// <param name="body_index">ID or number of the body detected by Kinect</param>
        private void publish_human_states(int body_index)
        {
            human_state[body_index].index = body_index; // TODO, this can be defined in other part
            pub_human.send_info(human_state[body_index]);

        }

        /// <summary>
        // Function used to send the audio state using ZMQ socket 
        /// </summary>
        /// <param name="person_number">ID or number of the person detected by Kinect</param>
        private void publish_audio_states(int person_number)
        {
            pub_sound.send_info(haudio);
        }
    }
}
