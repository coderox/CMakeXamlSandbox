#pragma once

// EGL includes
#include <EGL/egl.h>
#include <EGL/eglplatform.h>

class OpenGLES {
public:
	OpenGLES();
	virtual ~OpenGLES();

	void Initialize();
	EGLSurface CreateSurface(Windows::UI::Xaml::Controls::SwapChainPanel ^ panel, const Windows::Foundation::Size* renderSurfaceSize, const float* renderResolutionScale);
	void GetSurfaceDimensions(const EGLSurface surface, EGLint* width, EGLint* height);
	void DestroySurface(const EGLSurface surface);
	void MakeCurrent(const EGLSurface surface);
	EGLBoolean SwapBuffers(const EGLSurface surface);
	void Reset();

private:
	void Cleanup();

	EGLDisplay mEglDisplay;
	EGLContext mEglContext;
	EGLConfig mEglConfig;
};
