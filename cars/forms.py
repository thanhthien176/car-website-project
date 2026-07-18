from django import forms
from .models import Review

# class StarRatingWidget(forms.RadioSelect):
#     template_name = 'cars/widgets/_star_rating.html'

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} star") for i in range(1,6)],
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label="Đánh giá của bạn"
    )
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'title', 'content', 'pros', 'cons']
        labels = {
            'author_name': 'Email',
            'title': 'Tiêu đề ',
            'content': 'Nội dung',
            'pros': 'Ưu điểm',
            'cons': 'Nhược điểm'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Chia sẻ trải nghiệm thực tế của bạn với dòng xe này',
                }),
            'pros': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Điểm bạn thích ở dòng xe này',
                }),
            'cons': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Điểm bạn không thích ở dòng xe này',})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'rating':
                css_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{css_class} form-control"
            
        
    def save(self, commit=True):
        # commit=False: create instance but not yet INSERT into DB
        review = super().save(commit=False)
        review.is_approved = False
        if commit:
            review.save()
        return review