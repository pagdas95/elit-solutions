from django import forms

SERVICE_CHOICES = [
    ("", "Choose one"),
    ("website", "A website or web platform"),
    ("software", "Custom software / web application"),
    ("automation", "Business automation"),
    ("integration", "System integration"),
    ("other", "Something else / not sure yet"),
]
BUDGET_CHOICES = [
    ("", "Prefer not to say"),
    ("lt5", "Under €5,000"),
    ("5-15", "€5,000 – €15,000"),
    ("15-50", "€15,000 – €50,000"),
    ("gt50", "Over €50,000"),
]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"autocomplete": "name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    company = forms.CharField(max_length=160, required=False,
                              widget=forms.TextInput(attrs={"autocomplete": "organization"}))
    service = forms.ChoiceField(choices=SERVICE_CHOICES, label="What do you need?")
    budget = forms.ChoiceField(choices=BUDGET_CHOICES, required=False, label="Budget (optional)")
    message = forms.CharField(min_length=20, max_length=5000, label="Tell us about the project",
                              widget=forms.Textarea(attrs={"rows": 6}))
    # Honeypot: hidden from people, filled in by bots. A filled value silently discards the message.
    website = forms.CharField(required=False, label="Leave this field empty",
                              widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
